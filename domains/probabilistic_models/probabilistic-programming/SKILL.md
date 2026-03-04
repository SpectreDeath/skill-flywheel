---
Domain: probabilistic_models
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: probabilistic-programming
---



## Description

Automatically designs and implements optimal probabilistic programming systems for advanced Bayesian inference, model composition, and uncertainty quantification. This skill provides comprehensive frameworks for probabilistic programming languages, automatic differentiation variational inference, Hamiltonian Monte Carlo, and applications to scientific computing, machine learning, and decision analysis.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Probabilistic Programming Languages**: Implement DSLs for probabilistic modeling with automatic inference
- **Automatic Differentiation**: Design reverse-mode and forward-mode automatic differentiation for gradient-based inference
- **Variational Inference**: Create automatic differentiation variational inference (ADVI) and stochastic variational inference
- **Hamiltonian Monte Carlo**: Implement HMC, NUTS, and other advanced MCMC algorithms
- **Model Composition**: Design composable probabilistic models with hierarchical structures
- **Inference Compilation**: Create neural network-based proposal distributions for faster inference
- **Probabilistic Type Systems**: Implement type systems for probabilistic programs with uncertainty tracking

## Usage Examples

### Basic Probabilistic Programming Framework

```python
"""
Basic Probabilistic Programming Framework
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Set, Any, Optional, Callable, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod
import autograd.numpy as anp
from autograd import grad, jacobian
from scipy.optimize import minimize
from scipy.stats import norm, gamma, beta
import matplotlib.pyplot as plt

@dataclass
class RandomVariable:
    """Base class for random variables"""
    name: str
    distribution: str
    parameters: Dict[str, Union[float, 'RandomVariable']]
    value: Optional[float] = None
    
    def __repr__(self):
        return f"RV({self.name}: {self.distribution})"

class ProbabilisticModel:
    """Probabilistic programming model with automatic inference"""
    
    def __init__(self):
        self.variables: Dict[str, RandomVariable] = {}
        self.observations: Dict[str, float] = {}
        self.potential_functions: List[Callable] = []
        
    def add_variable(self, name: str, distribution: str, **parameters):
        """Add a random variable to the model"""
        rv = RandomVariable(name=name, distribution=distribution, parameters=parameters)
        self.variables[name] = rv
        return rv
    
    def observe(self, variable_name: str, value: float):
        """Add observation for a variable"""
        self.observations[variable_name] = value
    
    def add_potential(self, potential_fn: Callable):
        """Add a potential function (unnormalized log probability)"""
        self.potential_functions.append(potential_fn)
    
    def log_prob(self, values: Dict[str, float]) -> float:
        """Compute log probability of given values"""
        log_prob = 0.0
        
        # Add log probabilities from variables
        for name, rv in self.variables.items():
            if name in values:
                value = values[name]
                log_prob += self._compute_variable_log_prob(rv, value, values)
        
        # Add potential functions
        for potential_fn in self.potential_functions:
            log_prob += potential_fn(values)
        
        return log_prob
    
    def _compute_variable_log_prob(self, rv: RandomVariable, value: float, all_values: Dict[str, float]) -> float:
        """Compute log probability for a single variable"""
        # Resolve parameters (handle RandomVariable references)
        resolved_params = {}
        for param_name, param_value in rv.parameters.items():
            if isinstance(param_value, RandomVariable):
                if param_value.name in all_values:
                    resolved_params[param_name] = all_values[param_value.name]
                else:
                    raise ValueError(f"Parameter {param_name} depends on unobserved variable {param_value.name}")
            else:
                resolved_params[param_name] = param_value
        
        # Compute log probability based on distribution
        if rv.distribution == "normal":
            return norm.logpdf(value, loc=resolved_params.get("loc", 0.0), 
                              scale=resolved_params.get("scale", 1.0))
        elif rv.distribution == "gamma":
            return gamma.logpdf(value, a=resolved_params.get("a", 1.0), 
                               scale=resolved_params.get("scale", 1.0))
        elif rv.distribution == "beta":
            return beta.logpdf(value, a=resolved_params.get("a", 1.0), 
                              b=resolved_params.get("b", 1.0))
        else:
            raise ValueError(f"Unknown distribution: {rv.distribution}")
    
    def sample_prior(self, n_samples: int = 1) -> List[Dict[str, float]]:
        """Sample from the prior distribution"""
        samples = []
        
        for _ in range(n_samples):
            sample = {}
            
            # Sample each variable in topological order
            for name, rv in self.variables.items():
                sample[name] = self._sample_variable(rv, sample)
            
            samples.append(sample)
        
        return samples
    
    def _sample_variable(self, rv: RandomVariable, current_sample: Dict[str, float]) -> float:
        """Sample a single variable"""
        # Resolve parameters
        resolved_params = {}
        for param_name, param_value in rv.parameters.items():
            if isinstance(param_value, RandomVariable):
                resolved_params[param_name] = current_sample[param_value.name]
            else:
                resolved_params[param_name] = param_value
        
        # Sample based on distribution
        if rv.distribution == "normal":
            return norm.rvs(loc=resolved_params.get("loc", 0.0), 
                           scale=resolved_params.get("scale", 1.0))
        elif rv.distribution == "gamma":
            return gamma.rvs(a=resolved_params.get("a", 1.0), 
                            scale=resolved_params.get("scale", 1.0))
        elif rv.distribution == "beta":
            return beta.rvs(a=resolved_params.get("a", 1.0), 
                           b=resolved_params.get("b", 1.0))
        else:
            raise ValueError(f"Unknown distribution: {rv.distribution}")

class VariationalInference:
    """Automatic Differentiation Variational Inference (ADVI)"""
    
    def __init__(self, model: ProbabilisticModel):
        self.model = model
        self.q_params: Dict[str, Dict[str, float]] = {}
        
    def fit(self, n_iterations: int = 1000, learning_rate: float = 0.01):
        """Fit variational distribution using ADVI"""
        # Initialize variational parameters
        self._initialize_variational_params()
        
        # Optimization loop
        for iteration in range(n_iterations):
            # Sample from variational distribution
            samples = self._sample_variational(100)
            
            # Compute gradients
            gradients = self._compute_gradients(samples)
            
            # Update parameters
            for param_name in self.q_params:
                for param_key in self.q_params[param_name]:
                    self.q_params[param_name][param_key] += learning_rate * gradients[param_name][param_key]
            
            if iteration % 100 == 0:
                elbo = self._compute_elbo(samples)
                print(f"Iteration {iteration}, ELBO: {elbo:.4f}")
    
    def _initialize_variational_params(self):
        """Initialize variational parameters"""
        for name, rv in self.model.variables.items():
            if name not in self.model.observations:
                # Initialize with broad distributions
                if rv.distribution == "normal":
                    self.q_params[name] = {"loc": 0.0, "scale": 1.0}
                elif rv.distribution == "gamma":
                    self.q_params[name] = {"a": 1.0, "scale": 1.0}
                elif rv.distribution == "beta":
                    self.q_params[name] = {"a": 1.0, "b": 1.0}
    
    def _sample_variational(self, n_samples: int) -> List[Dict[str, float]]:
        """Sample from variational distribution"""
        samples = []
        
        for _ in range(n_samples):
            sample = {}
            for name, params in self.q_params.items():
                if params["scale"] > 0:  # Normal distribution
                    sample[name] = norm.rvs(loc=params["loc"], scale=params["scale"])
                else:  # Gamma distribution
                    sample[name] = gamma.rvs(a=params["a"], scale=params["scale"])
            samples.append(sample)
        
        return samples
    
    def _compute_gradients(self, samples: List[Dict[str, float]]) -> Dict[str, Dict[str, float]]:
        """Compute gradients of ELBO with respect to variational parameters"""
        gradients = {}
        
        for name in self.q_params:
            gradients[name] = {}
            for param_key in self.q_params[name]:
                gradients[name][param_key] = 0.0
        
        # Compute gradients using samples
        for sample in samples:
            # Log probability of model
            log_p = self.model.log_prob(sample)
            
            # Log probability of variational distribution
            log_q = 0.0
            for name, params in self.q_params.items():
                if name in sample:
                    if "scale" in params and params["scale"] > 0:
                        log_q += norm.logpdf(sample[name], loc=params["loc"], scale=params["scale"])
                    else:
                        log_q += gamma.logpdf(sample[name], a=params["a"], scale=params["scale"])
            
            # Gradient computation (simplified)
            # In practice, this would use automatic differentiation
            for name in self.q_params:
                for param_key in self.q_params[name]:
                    # This is a simplified gradient computation
                    # Real implementation would use autograd
                    gradients[name][param_key] += (log_p - log_q) * self._param_gradient(name, param_key, sample[name])
        
        # Average gradients
        for name in gradients:
            for param_key in gradients[name]:
                gradients[name][param_key] /= len(samples)
        
        return gradients
    
    def _param_gradient(self, name: str, param_key: str, value: float) -> float:
        """Compute gradient of log q with respect to parameter"""
        params = self.q_params[name]
        if param_key == "loc":
            return (value - params["loc"]) / params["scale"]**2
        elif param_key == "scale":
            return -(value - params["loc"])**2 / params["scale"]**3 + 1/params["scale"]
        else:
            return 0.0
    
    def _compute_elbo(self, samples: List[Dict[str, float]]) -> float:
        """Compute Evidence Lower BOund"""
        elbo = 0.0
        for sample in samples:
            log_p = self.model.log_prob(sample)
            log_q = 0.0
            for name, params in self.q_params.items():
                if name in sample:
                    if "scale" in params and params["scale"] > 0:
                        log_q += norm.logpdf(sample[name], loc=params["loc"], scale=params["scale"])
            elbo += log_p - log_q
        
        return elbo / len(samples)
    
    def predict(self, n_samples: int = 1000) -> Dict[str, np.ndarray]:
        """Generate predictions from fitted variational distribution"""
        samples = self._sample_variational(n_samples)
        
        predictions = {}
        for name in self.q_params:
            predictions[name] = np.array([sample[name] for sample in samples])
        
        return predictions

# Example usage
def example_probabilistic_programming():
    """Example: Bayesian linear regression using probabilistic programming"""
    
    # Generate synthetic data
    np.random.seed(42)
    n_data = 50
    true_slope = 2.0
    true_intercept = 1.0
    noise_std = 0.5
    
    x = np.linspace(0, 10, n_data)
    y = true_slope * x + true_intercept + np.random.normal(0, noise_std, n_data)
    
    # Define probabilistic model
    model = ProbabilisticModel()
    
    # Priors
    slope = model.add_variable("slope", "normal", loc=0.0, scale=10.0)
    intercept = model.add_variable("intercept", "normal", loc=0.0, scale=10.0)
    noise = model.add_variable("noise", "gamma", a=1.0, scale=1.0)
    
    # Likelihood
    for i, (xi, yi) in enumerate(zip(x, y)):
        mu = slope * xi + intercept
        model.add_variable(f"y_{i}", "normal", loc=mu, scale=noise)
        model.observe(f"y_{i}", yi)
    
    # Fit using variational inference
    vi = VariationalInference(model)
    vi.fit(n_iterations=2000, learning_rate=0.01)
    
    # Get predictions
    predictions = vi.predict(n_samples=1000)
    
    print("Posterior estimates:")
    for name in ["slope", "intercept", "noise"]:
        mean = np.mean(predictions[name])
        std = np.std(predictions[name])
        print(f"  {name}: {mean:.3f} ± {std:.3f}")
    
    print(f"\nTrue values:")
    print(f"  slope: {true_slope}")
    print(f"  intercept: {true_intercept}")
    print(f"  noise: {noise_std}")
    
    # Plot results
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 3, 1)
    plt.hist(predictions["slope"], bins=30, alpha=0.7, density=True)
    plt.axvline(true_slope, color='red', linestyle='--', label='True')
    plt.xlabel('Slope')
    plt.ylabel('Density')
    plt.legend()
    
    plt.subplot(1, 3, 2)
    plt.hist(predictions["intercept"], bins=30, alpha=0.7, density=True)
    plt.axvline(true_intercept, color='red', linestyle='--', label='True')
    plt.xlabel('Intercept')
    plt.ylabel('Density')
    plt.legend()
    
    plt.subplot(1, 3, 3)
    plt.hist(predictions["noise"], bins=30, alpha=0.7, density=True)
    plt.axvline(noise_std, color='red', linestyle='--', label='True')
    plt.xlabel('Noise')
    plt.ylabel('Density')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    return model, vi, predictions

if __name__ == "__main__":
    example_probabilistic_programming()
```

### Hamiltonian Monte Carlo Implementation

```python
"""
Hamiltonian Monte Carlo (HMC) Implementation
"""

import numpy as np
from typing import Dict, List, Tuple, Callable, Optional
from scipy.optimize import minimize
import matplotlib.pyplot as plt

class HamiltonianMonteCarlo:
    """Hamiltonian Monte Carlo sampler"""
    
    def __init__(self, log_prob_fn: Callable, grad_log_prob_fn: Callable):
        """
        Initialize HMC sampler
        
        Args:
            log_prob_fn: Function to compute log probability
            grad_log_prob_fn: Function to compute gradient of log probability
        """
        self.log_prob_fn = log_prob_fn
        self.grad_log_prob_fn = grad_log_prob_fn
        
    def sample(self, initial_state: np.ndarray, n_samples: int, 
               step_size: float = 0.01, n_leapfrog: int = 10) -> np.ndarray:
        """
        Generate samples using HMC
        
        Args:
            initial_state: Initial state vector
            n_samples: Number of samples to generate
            step_size: Step size for leapfrog integrator
            n_leapfrog: Number of leapfrog steps
            
        Returns:
            Array of samples
        """
        samples = np.zeros((n_samples, len(initial_state)))
        current_state = initial_state.copy()
        
        for i in range(n_samples):
            # Sample momentum
            momentum = np.random.normal(0, 1, len(current_state))
            current_momentum = momentum.copy()
            
            # Compute initial Hamiltonian
            current_log_prob = self.log_prob_fn(current_state)
            current_grad = self.grad_log_prob_fn(current_state)
            current_kinetic = 0.5 * np.sum(momentum**2)
            current_hamiltonian = -current_log_prob + current_kinetic
            
            # Leapfrog integration
            proposed_state = current_state.copy()
            proposed_momentum = momentum.copy()
            
            # Half step for momentum
            proposed_momentum += 0.5 * step_size * self.grad_log_prob_fn(proposed_state)
            
            # Full steps for position and momentum
            for _ in range(n_leapfrog):
                proposed_state += step_size * proposed_momentum
                if _ < n_leapfrog - 1:
                    proposed_momentum += step_size * self.grad_log_prob_fn(proposed_state)
            
            # Half step for momentum
            proposed_momentum += 0.5 * step_size * self.grad_log_prob_fn(proposed_state)
            
            # Compute proposed Hamiltonian
            proposed_log_prob = self.log_prob_fn(proposed_state)
            proposed_kinetic = 0.5 * np.sum(proposed_momentum**2)
            proposed_hamiltonian = -proposed_log_prob + proposed_kinetic
            
            # Metropolis acceptance
            acceptance_ratio = np.exp(current_hamiltonian - proposed_hamiltonian)
            
            if np.random.random() < min(1, acceptance_ratio):
                current_state = proposed_state
                current_log_prob = proposed_log_prob
            
            samples[i] = current_state
        
        return samples
    
    def find_reasonable_step_size(self, initial_state: np.ndarray, 
                                 target_accept: float = 0.65) -> float:
        """Find reasonable step size using dual averaging"""
        step_size = 1.0
        log_step_size = np.log(step_size)
        
        for i in range(100):
            # Sample using current step size
            samples = self.sample(initial_state, 10, step_size)
            
            # Compute acceptance rate
            # This is a simplified version - in practice you'd track acceptance during sampling
            acceptance_rate = 0.5  # Placeholder
            
            # Adjust step size
            if acceptance_rate < target_accept:
                log_step_size -= 2**(-i)
            else:
                log_step_size += 2**(-i)
            
            step_size = np.exp(log_step_size)
        
        return step_size

class NoUTurnSampler(HamiltonianMonteCarlo):
    """No-U-Turn Sampler (NUTS) - Adaptive HMC"""
    
    def __init__(self, log_prob_fn: Callable, grad_log_prob_fn: Callable):
        super().__init__(log_prob_fn, grad_log_prob_fn)
    
    def sample_nuts(self, initial_state: np.ndarray, n_samples: int) -> np.ndarray:
        """Generate samples using NUTS"""
        samples = np.zeros((n_samples, len(initial_state)))
        current_state = initial_state.copy()
        
        # Find reasonable step size
        step_size = self.find_reasonable_step_size(initial_state)
        
        for i in range(n_samples):
            # Sample momentum
            momentum = np.random.normal(0, 1, len(current_state))
            
            # Build trajectory
            tree = self._build_tree(current_state, momentum, step_size)
            
            # Sample from trajectory
            if tree['log_sum_weight'] > -np.inf:
                log_u = np.log(np.random.random()) + tree['log_sum_weight']
                current_state = self._sample_tree(tree, log_u)
            
            samples[i] = current_state
        
        return samples
    
    def _build_tree(self, position: np.ndarray, momentum: np.ndarray, 
                   step_size: float, depth: int = 10) -> Dict:
        """Build trajectory tree for NUTS"""
        if depth == 0:
            # Base case: single leapfrog step
            new_position, new_momentum = self._leapfrog(position, momentum, step_size)
            
            return {
                'position': new_position,
                'momentum': new_momentum,
                'log_sum_weight': self._compute_log_sum_weight(position, momentum, new_position, new_momentum),
                'n_proposals': 1
            }
        else:
            # Recursive case: build left and right subtrees
            left_tree = self._build_tree(position, momentum, step_size, depth - 1)
            
            # Check for U-turn
            if self._check_u_turn(left_tree['position'], left_tree['momentum'], 
                                left_tree['position'], left_tree['momentum']):
                return left_tree
            
            right_tree = self._build_tree(left_tree['position'], left_tree['momentum'], 
                                        step_size, depth - 1)
            
            # Combine trees
            return self._combine_trees(left_tree, right_tree)
    
    def _leapfrog(self, position: np.ndarray, momentum: np.ndarray, 
                 step_size: float) -> Tuple[np.ndarray, np.ndarray]:
        """Single leapfrog step"""
        # Half step for momentum
        momentum += 0.5 * step_size * self.grad_log_prob_fn(position)
        
        # Full step for position
        position += step_size * momentum
        
        # Half step for momentum
        momentum += 0.5 * step_size * self.grad_log_prob_fn(position)
        
        return position, momentum
    
    def _compute_log_sum_weight(self, pos_old: np.ndarray, mom_old: np.ndarray,
                               pos_new: np.ndarray, mom_new: np.ndarray) -> float:
        """Compute log sum weight for trajectory"""
        old_hamiltonian = -self.log_prob_fn(pos_old) + 0.5 * np.sum(mom_old**2)
        new_hamiltonian = -self.log_prob_fn(pos_new) + 0.5 * np.sum(mom_new**2)
        
        return -abs(new_hamiltonian - old_hamiltonian)
    
    def _check_u_turn(self, pos1: np.ndarray, mom1: np.ndarray, 
                     pos2: np.ndarray, mom2: np.ndarray) -> bool:
        """Check if trajectory has made a U-turn"""
        return np.dot(pos2 - pos1, mom1) < 0 or np.dot(pos2 - pos1, mom2) < 0
    
    def _combine_trees(self, left_tree: Dict, right_tree: Dict) -> Dict:
        """Combine two trajectory trees"""
        return {
            'position': right_tree['position'],
            'momentum': right_tree['momentum'],
            'log_sum_weight': self._log_sum_exp(left_tree['log_sum_weight'], right_tree['log_sum_weight']),
            'n_proposals': left_tree['n_proposals'] + right_tree['n_proposals']
        }
    
    def _log_sum_exp(self, a: float, b: float) -> float:
        """Numerically stable log sum exp"""
        if a > b:
            return a + np.log1p(np.exp(b - a))
        else:
            return b + np.log1p(np.exp(a - b))
    
    def _sample_tree(self, tree: Dict, log_u: float) -> np.ndarray:
        """Sample from trajectory tree"""
        if log_u <= tree['log_sum_weight']:
            return tree['position']
        else:
            # Recursively sample from subtrees
            return self._sample_tree(tree['left'], log_u) if np.random.random() < 0.5 else self._sample_tree(tree['right'], log_u)

# Example usage with HMC
def example_hamiltonian_monte_carlo():
    """Example: Sampling from a 2D Gaussian using HMC"""
    
    # Define 2D Gaussian
    mean = np.array([2.0, -1.0])
    cov = np.array([[1.0, 0.8], [0.8, 1.0]])
    inv_cov = np.linalg.inv(cov)
    
    def log_prob(x):
        """Log probability of 2D Gaussian"""
        diff = x - mean
        return -0.5 * diff.dot(inv_cov).dot(diff)
    
    def grad_log_prob(x):
        """Gradient of log probability"""
        diff = x - mean
        return -inv_cov.dot(diff)
    
    # Initialize HMC sampler
    hmc = HamiltonianMonteCarlo(log_prob, grad_log_prob)
    
    # Generate samples
    initial_state = np.array([0.0, 0.0])
    samples = hmc.sample(initial_state, 5000, step_size=0.1, n_leapfrog=20)
    
    # Plot results
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(samples[:, 0], samples[:, 1], alpha=0.5)
    plt.scatter(mean[0], mean[1], color='red', s=100, label='True mean')
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.title('HMC Samples')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.hist2d(samples[:, 0], samples[:, 1], bins=30, cmap='Blues')
    plt.colorbar()
    plt.scatter(mean[0], mean[1], color='red', s=100, label='True mean')
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.title('Sample Density')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Compute sample statistics
    sample_mean = np.mean(samples, axis=0)
    sample_cov = np.cov(samples.T)
    
    print("Sample statistics:")
    print(f"  Mean: {sample_mean}")
    print(f"  Covariance:\n{sample_cov}")
    print(f"\nTrue statistics:")
    print(f"  Mean: {mean}")
    print(f"  Covariance:\n{cov}")
    
    return samples

if __name__ == "__main__":
    example_hamiltonian_monte_carlo()
```

### Probabilistic Type System

```python
"""
Probabilistic Type System for Uncertainty Tracking
"""

from typing import Dict, List, Tuple, Optional, Union, TypeVar, Generic
from dataclasses import dataclass
import numpy as np

T = TypeVar('T')

@dataclass
class ProbabilisticType(Generic[T]):
    """Type representing a probabilistic value with uncertainty"""
    value: T
    uncertainty: float
    distribution_type: str = "normal"
    
    def __repr__(self):
        return f"Prob({self.value} ± {self.uncertainty})"

class ProbabilisticTypeChecker:
    """Type checker for probabilistic programs"""
    
    def __init__(self):
        self.type_env: Dict[str, ProbabilisticType] = {}
    
    def declare_variable(self, name: str, ptype: ProbabilisticType):
        """Declare a variable with probabilistic type"""
        self.type_env[name] = ptype
    
    def get_type(self, name: str) -> Optional[ProbabilisticType]:
        """Get type of variable"""
        return self.type_env.get(name)
    
    def check_binary_operation(self, op: str, left: ProbabilisticType, right: ProbabilisticType) -> ProbabilisticType:
        """Check binary operation and compute result type"""
        if op == "+":
            return self._add_types(left, right)
        elif op == "-":
            return self._subtract_types(left, right)
        elif op == "*":
            return self._multiply_types(left, right)
        elif op == "/":
            return self._divide_types(left, right)
        else:
            raise ValueError(f"Unknown operation: {op}")
    
    def _add_types(self, left: ProbabilisticType, right: ProbabilisticType) -> ProbabilisticType:
        """Add two probabilistic types"""
        result_value = left.value + right.value
        result_uncertainty = np.sqrt(left.uncertainty**2 + right.uncertainty**2)
        return ProbabilisticType(result_value, result_uncertainty)
    
    def _subtract_types(self, left: ProbabilisticType, right: ProbabilisticType) -> ProbabilisticType:
        """Subtract two probabilistic types"""
        result_value = left.value - right.value
        result_uncertainty = np.sqrt(left.uncertainty**2 + right.uncertainty**2)
        return ProbabilisticType(result_value, result_uncertainty)
    
    def _multiply_types(self, left: ProbabilisticType, right: ProbabilisticType) -> ProbabilisticType:
        """Multiply two probabilistic types"""
        result_value = left.value * right.value
        # Relative uncertainty propagation
        rel_uncertainty = np.sqrt((left.uncertainty/left.value)**2 + (right.uncertainty/right.value)**2)
        result_uncertainty = result_value * rel_uncertainty
        return ProbabilisticType(result_value, result_uncertainty)
    
    def _divide_types(self, left: ProbabilisticType, right: ProbabilisticType) -> ProbabilisticType:
        """Divide two probabilistic types"""
        result_value = left.value / right.value
        # Relative uncertainty propagation
        rel_uncertainty = np.sqrt((left.uncertainty/left.value)**2 + (right.uncertainty/right.value)**2)
        result_uncertainty = result_value * rel_uncertainty
        return ProbabilisticType(result_value, result_uncertainty)
    
    def check_function_call(self, func_name: str, args: List[ProbabilisticType]) -> ProbabilisticType:
        """Check function call and compute result type"""
        if func_name == "sin":
            return self._sin_type(args[0])
        elif func_name == "cos":
            return self._cos_type(args[0])
        elif func_name == "exp":
            return self._exp_type(args[0])
        elif func_name == "log":
            return self._log_type(args[0])
        else:
            raise ValueError(f"Unknown function: {func_name}")
    
    def _sin_type(self, arg: ProbabilisticType) -> ProbabilisticType:
        """Compute type of sin(arg)"""
        result_value = np.sin(arg.value)
        result_uncertainty = np.abs(np.cos(arg.value)) * arg.uncertainty
        return ProbabilisticType(result_value, result_uncertainty)
    
    def _cos_type(self, arg: ProbabilisticType) -> ProbabilisticType:
        """Compute type of cos(arg)"""
        result_value = np.cos(arg.value)
        result_uncertainty = np.abs(np.sin(arg.value)) * arg.uncertainty
        return ProbabilisticType(result_value, result_uncertainty)
    
    def _exp_type(self, arg: ProbabilisticType) -> ProbabilisticType:
        """Compute type of exp(arg)"""
        result_value = np.exp(arg.value)
        result_uncertainty = result_value * arg.uncertainty
        return ProbabilisticType(result_value, result_uncertainty)
    
    def _log_type(self, arg: ProbabilisticType) -> ProbabilisticType:
        """Compute type of log(arg)"""
        result_value = np.log(arg.value)
        result_uncertainty = arg.uncertainty / arg.value
        return ProbabilisticType(result_value, result_uncertainty)

class ProbabilisticProgram:
    """Probabilistic program with type checking"""
    
    def __init__(self):
        self.type_checker = ProbabilisticTypeChecker()
        self.statements = []
    
    def add_variable(self, name: str, value: float, uncertainty: float):
        """Add variable with uncertainty"""
        ptype = ProbabilisticType(value, uncertainty)
        self.type_checker.declare_variable(name, ptype)
        self.statements.append(f"var {name} = {ptype}")
    
    def add_binary_operation(self, result_name: str, op: str, left_name: str, right_name: str):
        """Add binary operation"""
        left_type = self.type_checker.get_type(left_name)
        right_type = self.type_checker.get_type(right_name)
        
        if left_type is None or right_type is None:
            raise ValueError("Undefined variables in operation")
        
        result_type = self.type_checker.check_binary_operation(op, left_type, right_type)
        self.type_checker.declare_variable(result_name, result_type)
        self.statements.append(f"{result_name} = {left_name} {op} {right_name}")
    
    def add_function_call(self, result_name: str, func_name: str, arg_name: str):
        """Add function call"""
        arg_type = self.type_checker.get_type(arg_name)
        
        if arg_type is None:
            raise ValueError("Undefined variable in function call")
        
        result_type = self.type_checker.check_function_call(func_name, [arg_type])
        self.type_checker.declare_variable(result_name, result_type)
        self.statements.append(f"{result_name} = {func_name}({arg_name})")
    
    def get_result_type(self, name: str) -> Optional[ProbabilisticType]:
        """Get type of result variable"""
        return self.type_checker.get_type(name)
    
    def print_program(self):
        """Print the program"""
        for statement in self.statements:
            print(statement)

# Example usage with probabilistic type system
def example_probabilistic_type_system():
    """Example: Uncertainty propagation in a physics calculation"""
    
    # Create probabilistic program
    program = ProbabilisticProgram()
    
    # Define measurements with uncertainties
    # Example: Calculate the area of a rectangle with uncertain dimensions
    program.add_variable("length", 10.0, 0.1)      # length ± uncertainty
    program.add_variable("width", 5.0, 0.05)       # width ± uncertainty
    
    # Calculate area = length * width
    program.add_binary_operation("area", "*", "length", "width")
    
    # Calculate perimeter = 2 * (length + width)
    program.add_binary_operation("perimeter_sum", "+", "length", "width")
    program.add_binary_operation("perimeter", "*", "perimeter_sum", "2.0")
    
    # Calculate diagonal = sqrt(length^2 + width^2)
    program.add_binary_operation("length_sq", "*", "length", "length")
    program.add_binary_operation("width_sq", "*", "width", "width")
    program.add_binary_operation("diagonal_sq", "+", "length_sq", "width_sq")
    program.add_function_call("diagonal", "sqrt", "diagonal_sq")
    
    # Print program
    print("Probabilistic Program:")
    program.print_program()
    print()
    
    # Print results with uncertainties
    print("Results with Uncertainties:")
    for var_name in ["area", "perimeter", "diagonal"]:
        result_type = program.get_result_type(var_name)
        if result_type:
            print(f"  {var_name}: {result_type.value:.3f} ± {result_type.uncertainty:.3f}")
    
    # Compare with analytical calculation
    print("\nAnalytical Verification:")
    length, width = 10.0, 5.0
    length_unc, width_unc = 0.1, 0.05
    
    # Area
    area = length * width
    area_unc = area * np.sqrt((length_unc/length)**2 + (width_unc/width)**2)
    print(f"  Area: {area:.3f} ± {area_unc:.3f}")
    
    # Perimeter
    perimeter = 2 * (length + width)
    perimeter_unc = 2 * np.sqrt(length_unc**2 + width_unc**2)
    print(f"  Perimeter: {perimeter:.3f} ± {perimeter_unc:.3f}")
    
    # Diagonal
    diagonal = np.sqrt(length**2 + width**2)
    diagonal_unc = diagonal * np.sqrt((length*length_unc)**2 + (width*width_unc)**2) / (length**2 + width**2)
    print(f"  Diagonal: {diagonal:.3f} ± {diagonal_unc:.3f}")
    
    return program

if __name__ == "__main__":
    example_probabilistic_type_system()
```

## Input Format

### Probabilistic Programming Configuration

```yaml
probabilistic_programming_config:
  language_type: "dsl|embedded|domain_specific"
  
  inference_config:
    method: "variational|monte_carlo|hybrid"
    variational_config:
      algorithm: "advi|svgd|normalizing_flows"
      optimization: "gradient_descent|adam|lbfgs"
      num_iterations: number
      learning_rate: number
    monte_carlo_config:
      algorithm: "hmc|nuts|metropolis|gibbs"
      num_samples: number
      warmup_samples: number
      step_size: number
      num_leapfrog_steps: number
  
  model_config:
    model_type: "bayesian|hierarchical|state_space|gaussian_process"
    parameter_priors: dict
    likelihood_function: string
    hierarchical_structure: dict
    
  compilation_config:
    automatic_differentiation: "forward|reverse|mixed"
    graph_optimization: boolean
    jit_compilation: boolean
    parallel_execution: boolean
```

### Advanced Configuration

```yaml
advanced_pp_config:
  neural_probabilistic_programs:
    neural_network_architecture: string # Architecture for neural components
    parameter_sharing: boolean          # Whether to share parameters between neural and probabilistic components
    training_strategy: string           # How to train neural probabilistic programs
    
  differentiable_programming:
    gradient_computation: string        # Method for gradient computation
    higher_order_derivatives: boolean   # Whether to support higher-order derivatives
    automatic_tuning: boolean           # Whether to automatically tune differentiation parameters
    
  probabilistic_deep_learning:
    integration_framework: string       # Framework for integrating with deep learning
    uncertainty_propagation: string     # Method for propagating uncertainty through neural networks
    regularization_techniques: array    # Regularization techniques for probabilistic deep learning
    
  scalable_inference:
    distributed_computation: boolean    # Use distributed computing for inference
    memory_optimization: boolean        # Optimize memory usage for large models
    streaming_inference: boolean        # Support for streaming data
```

## Output Format

### Model Compilation Results

```yaml
model_compilation_results:
  compiled_graph: dict              # Compiled computational graph
  optimized_parameters: dict        # Optimized model parameters
  compilation_time: number          # Time taken for compilation
  memory_usage: string              # Memory usage during compilation
  
  graph_properties:
    number_of_nodes: number         # Number of nodes in computational graph
    number_of_edges: number         # Number of edges in computational graph
    graph_depth: number             # Depth of computational graph
    parallelizable_operations: number # Number of operations that can be parallelized
```

### Inference Results

```yaml
inference_results:
  posterior_samples: array          # Samples from posterior distribution
  parameter_estimates: dict         # Point estimates of parameters
  uncertainty_quantification: dict  # Uncertainty measures for parameters
  convergence_metrics: dict         # Metrics for convergence assessment
  
  sampling_statistics:
    effective_sample_size: dict     # Effective sample size for each parameter
    r_hat_statistics: dict          # R-hat convergence statistics
    acceptance_rate: number         # Acceptance rate of sampling algorithm
    autocorrelation_time: dict      # Autocorrelation time for each parameter
```

### Performance Metrics

```yaml
performance_metrics:
  inference_speed: number           # Samples per second
  memory_efficiency: number         # Memory usage per sample
  convergence_rate: number          # Rate of convergence
  accuracy_metrics: dict            # Accuracy of inference results
  
  scalability_metrics:
    model_size_scaling: string      # How performance scales with model size
    data_size_scaling: string       # How performance scales with data size
    parallelization_efficiency: number # Efficiency of parallel execution
```

### Type System Results

```yaml
type_system_results:
  type_inferences: dict             # Inferred types for all variables
  uncertainty_propagation: dict     # How uncertainty propagates through the program
  type_errors: array                # Any type errors detected
  type_warnings: array              # Any type warnings
  
  type_safety_metrics:
    type_coverage: number           # Percentage of variables with type information
    uncertainty_coverage: number    # Percentage of variables with uncertainty information
    type_consistency: boolean       # Whether all types are consistent
```

## Configuration Options

### Inference Algorithms

```yaml
inference_algorithms:
  variational_inference:
    automatic_differentiation_variational_inference:
      description: "Gradient-based variational inference"
      best_for: ["large_models", "fast_inference", "approximate_posteriors"]
      complexity: "O(iterations * model_size)"
      parameters: ["learning_rate", "num_iterations", "variational_family"]
    
    stochastic_variational_inference:
      description: "SVI for large datasets"
      best_for: ["large_datasets", "online_learning", "scalability"]
      complexity: "O(minibatch_size * model_size)"
      parameters: ["minibatch_size", "learning_rate_schedule"]
    
    normalizing_flows:
      description: "Flexible variational families using normalizing flows"
      best_for: ["complex_posteriors", "flexible_approximations", "high_accuracy"]
      complexity: "O(flow_depth * model_size)"
      parameters: ["flow_type", "flow_depth", "base_distribution"]
  
  monte_carlo_methods:
    hamiltonian_monte_carlo:
      description: "HMC for efficient sampling"
      best_for: ["high_dimensional_spaces", "correlated_parameters", "efficient_sampling"]
      complexity: "O(leapfrog_steps * model_size)"
      parameters: ["step_size", "num_leapfrog_steps", "trajectory_length"]
    
    no_u_turn_sampler:
      description: "NUTS for automatic tuning"
      best_for: ["automatic_tuning", "adaptive_sampling", "robust_performance"]
      complexity: "O(log(tree_depth) * model_size)"
      parameters: ["target_acceptance_rate", "max_tree_depth"]
    
    sequential_monte_carlo:
      description: "SMC for sequential data"
      best_for: ["sequential_data", "state_space_models", "filtering"]
      complexity: "O(particles * model_size)"
      parameters: ["num_particles", "resampling_threshold"]
```

### Probabilistic Programming Languages

```yaml
probabilistic_programming_languages:
  stan:
    description: "Full-featured PPL with HMC/NUTS"
    best_for: ["statistical_modeling", "bayesian_inference", "mcmc_sampling"]
    features: ["automatic_differentiation", "hmc_sampling", "variational_inference"]
  
  pyro:
    description: "Deep probabilistic programming with PyTorch"
    best_for: ["deep_learning_integration", "neural_networks", "flexible_modeling"]
    features: ["stochastic_variational_inference", "normalizing_flows", "plate_notation"]
  
  tensorflow_probability:
    description: "Probabilistic programming with TensorFlow"
    best_for: ["tensorflow_integration", "scalable_inference", "production_systems"]
    features: ["variational_inference", "mcmc", "probabilistic_layers"]
  
  pymc:
    description: "Python probabilistic programming"
    best_for: ["statistical_modeling", "bayesian_analysis", "research_prototyping"]
    features: ["mcmc_sampling", "variational_inference", "model_comparison"]
```

## Error Handling

### Compilation Errors

```yaml
compilation_errors:
  syntax_errors:
    detection_strategy: "parser_validation"
    recovery_strategy: "syntax_correction"
    max_retries: 1
    fallback_action: "error_report"
  
  type_errors:
    detection_strategy: "type_inference"
    recovery_strategy: "type_inference"
    max_retries: 2
    fallback_action: "type_annotation_required"
  
  semantic_errors:
    detection_strategy: "semantic_analysis"
    recovery_strategy: "constraint_relaxation"
    max_retries: 1
    fallback_action: "manual_intervention_required"
```

### Inference Failures

```yaml
inference_failures:
  convergence_failure:
    detection_strategy: "convergence_monitoring"
    recovery_strategy: "parameter_adaptation"
    max_retries: 3
    fallback_action: "alternative_algorithm"
  
  numerical_instability:
    detection_strategy: "numerical_range_checking"
    recovery_strategy: "regularization"
    max_retries: 2
    fallback_action: "simplified_model"
  
  memory_exhaustion:
    detection_strategy: "memory_usage_monitoring"
    recovery_strategy: "memory_optimization"
    max_retries: 1
    fallback_action: "distributed_computation"
```

## Performance Optimization

### Algorithm Optimization

```python
# Optimization: Efficient automatic differentiation
class OptimizedAutomaticDifferentiation:
    """Optimized automatic differentiation for probabilistic programming"""
    
    def __init__(self):
        self.computation_graph = None
        self.gradient_cache = {}
    
    def build_computation_graph(self, function):
        """Build optimized computation graph"""
        # Use graph optimization techniques
        # - Common subexpression elimination
        # - Operation fusion
        # - Memory layout optimization
        pass
    
    def compute_gradients(self, variables):
        """Compute gradients efficiently"""
        # Use reverse-mode AD with optimizations
        # - Gradient checkpointing
        # - Sparse gradient computation
        # - Parallel gradient computation
        pass
    
    def hessian_vector_product(self, function, vector):
        """Compute Hessian-vector products efficiently"""
        # Use forward-over-reverse AD
        # Optimized for second-order methods
        pass
```

### Memory Optimization

```yaml
memory_optimization:
  gradient_checkpointing:
    technique: "memory_computation_tradeoff"
    memory_reduction: "50-80%"
    implementation: "gradient_recomputation"
    
  sparse_computation:
    technique: "sparse_matrix_operations"
    memory_reduction: "60-90%"
    implementation: "compressed_sparse_format"
    
  streaming_computation:
    technique: "online_processing"
    memory_reduction: "unlimited_data"
    implementation: "incremental_updates"
    
  distributed_memory:
    technique: "cluster_memory_sharing"
    memory_reduction: "cluster_scaling"
    implementation: "distributed_storage"
```

## Integration Examples

### With Scientific Computing

```python
# Integration with scientific computing for differential equations
class ProbabilisticDifferentialEquations:
    """Probabilistic programming for differential equation models"""
    
    def __init__(self):
        self.model = ProbabilisticModel()
    
    def add_differential_equation(self, variable, derivative_fn, initial_value, uncertainty):
        """Add differential equation with uncertainty"""
        # Define initial condition as random variable
        initial_rv = self.model.add_variable(f"{variable}_0", "normal", 
                                           loc=initial_value, scale=uncertainty)
        
        # Define differential equation
        # In practice, this would integrate with ODE solvers
        pass
    
    def solve_probabilistic_ode(self, time_points):
        """Solve ODE with uncertainty quantification"""
        # Use probabilistic numerical methods
        # - Gaussian process ODE solvers
        # - Uncertainty propagation through numerical integration
        pass
```

### With Machine Learning

```python
# Integration with machine learning for probabilistic neural networks
class ProbabilisticNeuralNetworks:
    """Probabilistic programming for neural network uncertainty"""
    
    def __init__(self):
        self.model = ProbabilisticModel()
    
    def add_probabilistic_layer(self, layer_name, input_dim, output_dim, prior_scale=1.0):
        """Add layer with probabilistic weights"""
        # Define weight matrix as random variables
        for i in range(input_dim):
            for j in range(output_dim):
                weight_name = f"{layer_name}_w_{i}_{j}"
                self.model.add_variable(weight_name, "normal", loc=0.0, scale=prior_scale)
    
    def add_dropout_layer(self, layer_name, dropout_rate):
        """Add dropout as probabilistic operation"""
        # Model dropout as Bernoulli random variables
        pass
    
    def train_with_uncertainty(self, training_data, num_samples=1000):
        """Train network with uncertainty quantification"""
        # Use variational inference or MCMC for training
        pass
```

## Best Practices

1. **Model Design**:
   - Use appropriate priors based on domain knowledge
   - Design hierarchical models for complex data structures
   - Validate model assumptions with posterior predictive checks

2. **Inference Selection**:
   - Use variational inference for large models and fast inference
   - Use MCMC for accurate posterior estimation when time allows
   - Consider hybrid methods for complex models

3. **Computational Efficiency**:
   - Use automatic differentiation for gradient computation
   - Implement efficient sampling algorithms
   - Optimize memory usage for large-scale problems

4. **Validation and Diagnostics**:
   - Check convergence of sampling algorithms
   - Validate model fit with posterior predictive checks
   - Use cross-validation for model comparison

## Troubleshooting

### Common Issues

1. **Poor Convergence**: Check step sizes, increase samples, use better initialization
2. **High Memory Usage**: Use gradient checkpointing, sparse representations, distributed computing
3. **Slow Inference**: Use variational methods, optimize model structure, parallelize computation
4. **Numerical Instability**: Add regularization, check parameter bounds, use stable implementations

### Debug Mode

```python
# Debug mode: Enhanced probabilistic programming debugging
class DebugProbabilisticProgramming:
    """Probabilistic programming with enhanced debugging capabilities"""
    
    def __init__(self, model):
        self.model = model
        self.debug_log = []
        self.convergence_analysis = {}
        self.sensitivity_analysis = {}
    
    def log_inference_step(self, step_data):
        """Log detailed inference information"""
        self.debug_log.append({
            'iteration': step_data['iteration'],
            'log_likelihood': step_data['log_likelihood'],
            'gradient_norm': step_data['gradient_norm'],
            'acceptance_rate': step_data.get('acceptance_rate', 0.0),
            'memory_usage': step_data['memory_usage']
        })
    
    def analyze_convergence(self):
        """Analyze convergence patterns and issues"""
        self.convergence_analysis = {
            'effective_sample_size': self._compute_effective_sample_size(),
            'r_hat_statistics': self._compute_r_hat_statistics(),
            'autocorrelation_analysis': self._analyze_autocorrelation(),
            'convergence_diagnostics': self._compute_convergence_diagnostics()
        }
        
        return self.convergence_analysis
    
    def generate_debug_report(self):
        """Generate comprehensive debug report"""
        return {
            'convergence_analysis': self.analyze_convergence(),
            'sensitivity_analysis': self.analyze_sensitivity(),
            'performance_metrics': self.get_performance_metrics(),
            'recommendations': self.get_optimization_recommendations()
        }
```

## Monitoring and Metrics

### Probabilistic Programming Performance Metrics

```yaml
probabilistic_programming_metrics:
  compilation_metrics:
    compilation_time: number        # Time to compile probabilistic program
    graph_optimization_gain: number # Improvement from graph optimization
    memory_usage_peak: string       # Peak memory usage during compilation
    parallelization_factor: number  # Degree of parallelization achieved
  
  inference_metrics:
    samples_per_second: number      # Sampling speed
    effective_sample_size: number   # Effective sample size
    convergence_time: number        # Time to convergence
    accuracy_error: number          # Error in inference results
  
  type_system_metrics:
    type_inference_time: number     # Time for type inference
    uncertainty_propagation_accuracy: number # Accuracy of uncertainty propagation
    type_safety_violations: number  # Number of type safety violations
    type_coverage: number           # Percentage of typed variables
  
  scalability_metrics:
    model_size_scaling: string      # Performance scaling with model size
    data_size_scaling: string       # Performance scaling with data size
    parallel_efficiency: number     # Efficiency of parallel execution
    memory_scaling: string          # Memory usage scaling
```

## Dependencies

- **Core Libraries**: NumPy, SciPy for mathematical operations
- **Automatic Differentiation**: Autograd, JAX for gradient computation
- **Optimization**: CVXPY, Pyomo for parameter optimization
- **Probabilistic Programming**: PyMC, Stan, Pyro for advanced PPL features
- **Machine Learning**: PyTorch, TensorFlow for neural network integration
- **Visualization**: Matplotlib, Plotly for result visualization

## Version History

- **1.0.0**: Initial release with comprehensive probabilistic programming frameworks
- **1.1.0**: Added automatic differentiation variational inference and HMC implementations
- **1.2.0**: Enhanced probabilistic type systems and uncertainty quantification
- **1.3.0**: Improved performance optimization and memory management
- **1.4.0**: Added neural probabilistic programming and differentiable programming
- **1.5.0**: Enhanced debugging tools and model validation techniques

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

To be provided dynamically during execution.