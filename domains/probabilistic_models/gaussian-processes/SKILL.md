---
Domain: probabilistic_models
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: gaussian-processes
---



## Description

Automatically designs and implements optimal Gaussian processes for regression, classification, and uncertainty quantification. This skill provides comprehensive frameworks for kernel design, hyperparameter optimization, sparse approximations, multi-output processes, and scalable implementations for large datasets.


## Purpose

*[Content for Purpose section to be added based on the specific skill requirements]*

## Examples

*[Content for Examples section to be added based on the specific skill requirements]*

## Implementation Notes

*[Content for Implementation Notes section to be added based on the specific skill requirements]*
## Capabilities

- **Kernel Design**: Implement diverse kernel functions (RBF, Matérn, periodic, composite) with automatic selection
- **Hyperparameter Optimization**: Design gradient-based and derivative-free optimization for kernel parameters
- **Sparse Approximations**: Create variational inference, inducing point methods, and structured approximations
- **Multi-output Processes**: Design multi-task learning, coregionalization, and convolution processes
- **Uncertainty Quantification**: Implement predictive uncertainty, confidence intervals, and calibration
- **Scalability**: Design efficient algorithms for large datasets with O(n log n) complexity
- **Active Learning**: Implement acquisition functions for optimal data selection

## Usage Examples

### Basic Gaussian Process Regression

```python
"""
Basic Gaussian Process Regression Framework
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Set, Any, Optional
from dataclasses import dataclass
from scipy.optimize import minimize
from scipy.linalg import cholesky, solve, det
import matplotlib.pyplot as plt

@dataclass
class Kernel:
    """Base kernel class"""
    name: str
    parameters: Dict[str, float]
    
    def compute(self, X1: np.ndarray, X2: np.ndarray) -> np.ndarray:
        """Compute kernel matrix between X1 and X2"""
        raise NotImplementedError
    
    def gradient(self, X1: np.ndarray, X2: np.ndarray) -> Dict[str, np.ndarray]:
        """Compute gradients with respect to parameters"""
        raise NotImplementedError

class RBFKernel(Kernel):
    """Radial Basis Function (Squared Exponential) kernel"""
    
    def __init__(self, lengthscale: float = 1.0, variance: float = 1.0):
        super().__init__("RBF", {"lengthscale": lengthscale, "variance": variance})
    
    def compute(self, X1: np.ndarray, X2: np.ndarray) -> np.ndarray:
        """Compute RBF kernel matrix"""
        if X1.ndim == 1:
            X1 = X1.reshape(-1, 1)
        if X2.ndim == 1:
            X2 = X2.reshape(-1, 1)
        
        # Compute squared distances
        dist_sq = np.sum(X1**2, 1).reshape(-1, 1) + np.sum(X2**2, 1) - 2 * X1.dot(X2.T)
        
        lengthscale = self.parameters["lengthscale"]
        variance = self.parameters["variance"]
        
        return variance * np.exp(-0.5 * dist_sq / lengthscale**2)
    
    def gradient(self, X1: np.ndarray, X2: np.ndarray) -> Dict[str, np.ndarray]:
        """Compute gradients with respect to parameters"""
        K = self.compute(X1, X2)
        
        lengthscale = self.parameters["lengthscale"]
        
        grad_lengthscale = K * (np.sum((X1[:, np.newaxis] - X2[np.newaxis, :])**2, axis=2) / lengthscale**3)
        grad_variance = K / self.parameters["variance"]
        
        return {
            "lengthscale": grad_lengthscale,
            "variance": grad_variance
        }

class MaternKernel(Kernel):
    """Matérn kernel with nu parameter"""
    
    def __init__(self, lengthscale: float = 1.0, variance: float = 1.0, nu: float = 1.5):
        super().__init__("Matern", {"lengthscale": lengthscale, "variance": variance, "nu": nu})
    
    def compute(self, X1: np.ndarray, X2: np.ndarray) -> np.ndarray:
        """Compute Matérn kernel matrix"""
        from scipy.special import kv, gamma
        
        if X1.ndim == 1:
            X1 = X1.reshape(-1, 1)
        if X2.ndim == 1:
            X2 = X2.reshape(-1, 1)
        
        # Compute distances
        dist = np.sqrt(np.sum((X1[:, np.newaxis] - X2[np.newaxis, :])**2, axis=2))
        
        lengthscale = self.parameters["lengthscale"]
        variance = self.parameters["variance"]
        nu = self.parameters["nu"]
        
        # Matérn kernel formula
        dist_scaled = np.sqrt(2 * nu) * dist / lengthscale
        
        # Handle zero distance
        dist_scaled[dist_scaled == 0] = 1e-10
        
        # Bessel function and gamma function
        K_nu = kv(nu, dist_scaled)
        gamma_nu = gamma(nu)
        
        coefficient = 2**(1 - nu) / gamma_nu
        
        return variance * coefficient * (dist_scaled**nu) * K_nu

class GaussianProcess:
    """Gaussian Process Regression implementation"""
    
    def __init__(self, kernel: Kernel, noise_variance: float = 1e-3):
        """
        Initialize Gaussian Process
        
        Args:
            kernel: Kernel function
            noise_variance: Observation noise variance
        """
        self.kernel = kernel
        self.noise_variance = noise_variance
        self.X_train = None
        self.y_train = None
        self.K_inv = None
        self.log_marginal_likelihood = None
    
    def fit(self, X: np.ndarray, y: np.ndarray, optimize_hyperparameters: bool = True):
        """
        Fit Gaussian Process to training data
        
        Args:
            X: Training inputs (n_samples, n_features)
            y: Training outputs (n_samples,)
            optimize_hyperparameters: Whether to optimize kernel parameters
        """
        self.X_train = X if X.ndim == 2 else X.reshape(-1, 1)
        self.y_train = y
        
        if optimize_hyperparameters:
            self._optimize_hyperparameters()
        
        # Compute kernel matrix
        K = self.kernel.compute(self.X_train, self.X_train)
        K += self.noise_variance * np.eye(len(self.X_train))
        
        # Cholesky decomposition for numerical stability
        try:
            L = cholesky(K, lower=True)
            self.K_inv = solve(L.T, solve(L, np.eye(len(self.X_train))))
        except np.linalg.LinAlgError:
            # Fall back to direct inversion if Cholesky fails
            self.K_inv = np.linalg.inv(K)
        
        # Compute log marginal likelihood
        self.log_marginal_likelihood = -0.5 * (
            self.y_train.T.dot(self.K_inv).dot(self.y_train) +
            np.log(det(K)) +
            len(self.y_train) * np.log(2 * np.pi)
        )
    
    def predict(self, X_test: np.ndarray, return_std: bool = True, 
                return_cov: bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions on test data
        
        Args:
            X_test: Test inputs (n_test_samples, n_features)
            return_std: Whether to return standard deviations
            return_cov: Whether to return full covariance matrix
            
        Returns:
            mean: Predictive mean
            std or cov: Predictive standard deviation or covariance
        """
        X_test = X_test if X_test.ndim == 2 else X_test.reshape(-1, 1)
        
        # Compute cross-covariance
        K_star = self.kernel.compute(self.X_train, X_test)
        
        # Predictive mean
        mean = K_star.T.dot(self.K_inv).dot(self.y_train)
        
        if return_cov:
            # Full covariance matrix
            K_test = self.kernel.compute(X_test, X_test)
            cov = K_test - K_star.T.dot(self.K_inv).dot(K_star)
            return mean, cov
        elif return_std:
            # Standard deviations only
            K_test_diag = np.diag(self.kernel.compute(X_test, X_test))
            var = K_test_diag - np.sum((K_star.T.dot(self.K_inv)) * K_star.T, axis=1)
            std = np.sqrt(np.maximum(var, 1e-10))  # Ensure positive variance
            return mean, std
        else:
            return mean, None
    
    def _optimize_hyperparameters(self):
        """Optimize kernel hyperparameters using gradient descent"""
        def objective(params):
            # Set parameters
            for i, param_name in enumerate(self.kernel.parameters.keys()):
                self.kernel.parameters[param_name] = params[i]
            
            # Compute kernel matrix
            K = self.kernel.compute(self.X_train, self.X_train)
            K += self.noise_variance * np.eye(len(self.X_train))
            
            try:
                # Cholesky decomposition
                L = cholesky(K, lower=True)
                alpha = solve(L.T, solve(L, self.y_train))
                
                # Log marginal likelihood
                log_likelihood = -0.5 * (
                    self.y_train.dot(alpha) +
                    np.sum(np.log(np.diag(L))) +
                    len(self.y_train) * np.log(2 * np.pi)
                )
                
                return -log_likelihood  # Minimize negative log likelihood
            except np.linalg.LinAlgError:
                return 1e6  # Large penalty for invalid parameters
        
        def gradient(params):
            # Set parameters
            for i, param_name in enumerate(self.kernel.parameters.keys()):
                self.kernel.parameters[param_name] = params[i]
            
            # Compute kernel matrix and its inverse
            K = self.kernel.compute(self.X_train, self.X_train)
            K += self.noise_variance * np.eye(len(self.X_train))
            K_inv = np.linalg.inv(K)
            
            # Compute alpha
            alpha = K_inv.dot(self.y_train)
            
            # Compute gradients
            grads = self.kernel.gradient(self.X_train, self.X_train)
            
            grad_params = []
            for param_name in self.kernel.parameters.keys():
                # Gradient of log marginal likelihood
                grad = -0.5 * (
                    alpha.dot(grads[param_name].dot(alpha)) -
                    np.trace(K_inv.dot(grads[param_name]))
                )
                grad_params.append(grad)
            
            return np.array(grad_params)
        
        # Initial parameters
        initial_params = list(self.kernel.parameters.values())
        
        # Optimization bounds
        bounds = [(1e-5, 100)] * len(initial_params)
        
        # Optimize
        result = minimize(
            objective,
            initial_params,
            method='L-BFGS-B',
            jac=gradient,
            bounds=bounds,
            options={'maxiter': 100, 'disp': False}
        )
        
        # Update parameters
        for i, param_name in enumerate(self.kernel.parameters.keys()):
            self.kernel.parameters[param_name] = result.x[i]

# Example usage
def example_gaussian_process_regression():
    """Example: Gaussian Process Regression on noisy sine function"""
    
    # Generate training data
    np.random.seed(42)
    X_train = np.linspace(0, 10, 20)
    y_train = np.sin(X_train) + 0.1 * np.random.randn(20)
    
    # Create GP with RBF kernel
    kernel = RBFKernel(lengthscale=1.0, variance=1.0)
    gp = GaussianProcess(kernel, noise_variance=0.01)
    
    # Fit GP
    gp.fit(X_train, y_train, optimize_hyperparameters=True)
    
    print("Optimized kernel parameters:")
    for param, value in gp.kernel.parameters.items():
        print(f"  {param}: {value:.3f}")
    print(f"Log marginal likelihood: {gp.log_marginal_likelihood:.3f}")
    
    # Make predictions
    X_test = np.linspace(-2, 12, 100)
    mean, std = gp.predict(X_test, return_std=True)
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(X_test, np.sin(X_test), 'r--', label='True function')
    plt.plot(X_train, y_train, 'ko', label='Training data')
    plt.plot(X_test, mean, 'b-', label='GP prediction')
    plt.fill_between(X_test, mean - 2*std, mean + 2*std, alpha=0.3, color='blue', label='95% confidence')
    plt.legend()
    plt.title('Gaussian Process Regression')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return gp, X_test, mean, std

if __name__ == "__main__":
    example_gaussian_process_regression()
```

### Sparse Gaussian Process with Inducing Points

```python
"""
Sparse Gaussian Process with Variational Inference
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from scipy.optimize import minimize
from scipy.linalg import cholesky, solve

class SparseGaussianProcess:
    """Sparse Gaussian Process using Variational Inference"""
    
    def __init__(self, kernel, num_inducing: int = 10, noise_variance: float = 1e-3):
        """
        Initialize Sparse GP
        
        Args:
            kernel: Base kernel function
            num_inducing: Number of inducing points
            noise_variance: Observation noise variance
        """
        self.kernel = kernel
        self.num_inducing = num_inducing
        self.noise_variance = noise_variance
        self.X_train = None
        self.y_train = None
        self.Z = None  # Inducing points
        self.q_m = None  # Variational mean
        self.q_S = None  # Variational covariance
        self.K_mm = None  # Kernel matrix for inducing points
    
    def fit(self, X: np.ndarray, y: np.ndarray, optimize_hyperparameters: bool = True):
        """
        Fit Sparse GP using variational inference
        
        Args:
            X: Training inputs
            y: Training outputs
            optimize_hyperparameters: Whether to optimize parameters
        """
        self.X_train = X if X.ndim == 2 else X.reshape(-1, 1)
        self.y_train = y
        
        # Initialize inducing points
        self._initialize_inducing_points()
        
        if optimize_hyperparameters:
            self._optimize_parameters()
        else:
            self._optimize_variational_parameters()
    
    def _initialize_inducing_points(self):
        """Initialize inducing points using k-means++ or random selection"""
        # Simple random initialization
        n_samples = len(self.X_train)
        indices = np.random.choice(n_samples, self.num_inducing, replace=False)
        self.Z = self.X_train[indices].copy()
    
    def _compute_kernels(self):
        """Compute necessary kernel matrices"""
        # K_mm: inducing points covariance
        self.K_mm = self.kernel.compute(self.Z, self.Z)
        
        # K_mn: inducing-training covariance
        self.K_mn = self.kernel.compute(self.Z, self.X_train)
        
        # K_nn_diag: training points diagonal (for noise)
        self.K_nn_diag = np.diag(self.kernel.compute(self.X_train, self.X_train))
    
    def _optimize_variational_parameters(self):
        """Optimize variational parameters m and S"""
        self._compute_kernels()
        
        # Cholesky decomposition of K_mm
        L_mm = cholesky(self.K_mm, lower=True)
        
        # Compute K_mm^-1 * K_mn
        K_mm_inv_K_mn = solve(L_mm.T, solve(L_mm, self.K_mn))
        
        # Variational parameters
        # q(m) = K_mm^-1 * K_mn * y
        self.q_m = K_mm_inv_K_mn.dot(self.y_train)
        
        # q(S) = K_mm^-1 * (K_mm - K_mn * K_nm / (noise + K_nn)) * K_mm^-1
        # Simplified version for diagonal approximation
        temp = K_mm_inv_K_mn.dot(K_mm_inv_K_mn.T)
        self.q_S = self.K_mm - self.K_mm.dot(temp).dot(self.K_mm)
    
    def _variational_objective(self, params: np.ndarray) -> float:
        """Variational lower bound objective function"""
        # Set parameters
        for i, param_name in enumerate(self.kernel.parameters.keys()):
            self.kernel.parameters[param_name] = params[i]
        
        self._compute_kernels()
        self._optimize_variational_parameters()
        
        # Compute variational lower bound
        L = 0.0
        
        # Term 1: Expected log likelihood
        # For Gaussian likelihood, this has a closed form
        K_mm_inv = np.linalg.inv(self.K_mm)
        trace_term = np.trace(K_mm_inv.dot(self.q_S))
        
        # Expected log likelihood approximation
        mu_f = self.K_mn.T.dot(K_mm_inv).dot(self.q_m)
        var_f = self.K_nn_diag + np.sum(self.K_mn.T.dot(K_mm_inv).dot(self.q_S) * self.K_mn.T.dot(K_mm_inv), axis=1)
        
        expected_ll = -0.5 * np.sum((self.y_train - mu_f)**2 / (self.noise_variance + var_f) + 
                                   np.log(self.noise_variance + var_f))
        
        L += expected_ll
        
        # Term 2: KL divergence between q(u) and p(u)
        # KL[q(u) || p(u)] = 0.5 * (log|K_mm| - log|q_S| + tr(K_mm^-1 * q_S) - m^T * K_mm^-1 * m - M)
        log_det_K_mm = 2 * np.sum(np.log(np.diag(cholesky(self.K_mm, lower=True))))
        log_det_q_S = np.sum(np.log(np.diag(cholesky(self.q_S, lower=True))))
        
        kl_div = 0.5 * (log_det_K_mm - log_det_q_S + trace_term - 
                       self.q_m.T.dot(K_mm_inv).dot(self.q_m) - self.num_inducing)
        
        L -= kl_div
        
        return -L  # Minimize negative lower bound
    
    def _optimize_parameters(self):
        """Optimize hyperparameters and inducing points"""
        def objective(params):
            # Split parameters into kernel params and inducing point locations
            n_kernel_params = len(self.kernel.parameters)
            kernel_params = params[:n_kernel_params]
            inducing_params = params[n_kernel_params:]
            
            # Set kernel parameters
            for i, param_name in enumerate(self.kernel.parameters.keys()):
                self.kernel.parameters[param_name] = kernel_params[i]
            
            # Reshape inducing points
            self.Z = inducing_params.reshape(self.num_inducing, -1)
            
            return self._variational_objective(kernel_params)
        
        # Initial parameters
        kernel_params = list(self.kernel.parameters.values())
        inducing_params = self.Z.flatten()
        initial_params = kernel_params + inducing_params.tolist()
        
        # Optimization bounds
        n_kernel = len(kernel_params)
        bounds = [(1e-5, 100)] * n_kernel + [(-10, 10)] * len(inducing_params)
        
        # Optimize
        result = minimize(
            objective,
            initial_params,
            method='L-BFGS-B',
            bounds=bounds,
            options={'maxiter': 100}
        )
        
        # Update parameters
        optimized_params = result.x
        for i, param_name in enumerate(self.kernel.parameters.keys()):
            self.kernel.parameters[param_name] = optimized_params[i]
        
        self.Z = optimized_params[n_kernel:].reshape(self.num_inducing, -1)
        self._optimize_variational_parameters()
    
    def predict(self, X_test: np.ndarray, return_std: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """Make predictions using sparse GP"""
        X_test = X_test if X_test.ndim == 2 else X_test.reshape(-1, 1)
        
        # Compute kernel matrices
        K_mm = self.kernel.compute(self.Z, self.Z)
        K_mn = self.kernel.compute(self.Z, self.X_train)
        K_mt = self.kernel.compute(self.Z, X_test)
        
        # Cholesky decomposition
        L_mm = cholesky(K_mm, lower=True)
        
        # Predictive mean
        K_mm_inv = solve(L_mm.T, solve(L_mm, np.eye(self.num_inducing)))
        K_mm_inv_K_mn = K_mm_inv.dot(K_mn)
        K_mm_inv_K_mt = K_mm_inv.dot(K_mt)
        
        mean = K_mt.T.dot(K_mm_inv).dot(self.q_m)
        
        if return_std:
            # Predictive variance
            var = self.kernel.compute(X_test, X_test).diagonal()
            var += np.sum(K_mt.T.dot(K_mm_inv).dot(self.q_S) * K_mt.T.dot(K_mm_inv), axis=1)
            var -= np.sum(K_mt.T.dot(K_mm_inv_K_mt) * K_mt.T.dot(K_mm_inv_K_mt), axis=1)
            
            std = np.sqrt(np.maximum(var, 1e-10))
            return mean, std
        else:
            return mean, None

# Example usage with sparse GP
def example_sparse_gaussian_process():
    """Example: Sparse GP on large dataset"""
    
    # Generate large dataset
    np.random.seed(42)
    n_samples = 1000
    X_train = np.linspace(0, 20, n_samples)
    y_train = np.sin(X_train) + 0.1 * np.random.randn(n_samples)
    
    # Create sparse GP
    kernel = RBFKernel(lengthscale=2.0, variance=1.0)
    sgp = SparseGaussianProcess(kernel, num_inducing=50, noise_variance=0.01)
    
    # Fit sparse GP
    import time
    start_time = time.time()
    sgp.fit(X_train, y_train, optimize_hyperparameters=True)
    fit_time = time.time() - start_time
    
    print(f"Sparse GP fitting time: {fit_time:.3f} seconds")
    print("Optimized parameters:")
    for param, value in sgp.kernel.parameters.items():
        print(f"  {param}: {value:.3f}")
    
    # Make predictions
    X_test = np.linspace(-2, 22, 200)
    start_time = time.time()
    mean, std = sgp.predict(X_test, return_std=True)
    pred_time = time.time() - start_time
    
    print(f"Prediction time: {pred_time:.3f} seconds")
    
    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(X_train, y_train, 'k.', alpha=0.3, label='Training data')
    plt.plot(X_test, np.sin(X_test), 'r--', label='True function')
    plt.plot(X_test, mean, 'b-', label='Sparse GP prediction')
    plt.fill_between(X_test, mean - 2*std, mean + 2*std, alpha=0.3, color='blue')
    plt.plot(sgp.Z, np.zeros_like(sgp.Z), 'ro', markersize=8, label='Inducing points')
    plt.legend()
    plt.title('Sparse Gaussian Process Regression')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return sgp, X_test, mean, std

if __name__ == "__main__":
    example_sparse_gaussian_process()
```

### Multi-Output Gaussian Process

```python
"""
Multi-Output Gaussian Process with Linear Model of Coregionalization
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from scipy.linalg import cholesky, solve

class MultiOutputGP:
    """Multi-Output Gaussian Process using Linear Model of Coregionalization"""
    
    def __init__(self, kernel, num_tasks: int, num_latent: int = None):
        """
        Initialize Multi-Output GP
        
        Args:
            kernel: Base kernel function
            num_tasks: Number of output tasks
            num_latent: Number of latent processes (if None, equals num_tasks)
        """
        self.kernel = kernel
        self.num_tasks = num_tasks
        self.num_latent = num_latent if num_latent is not None else num_tasks
        
        # Coregionalization matrices
        self.B = None  # Task mixing matrix
        self.W = None  # Task-specific weights
        self.kappa = None  # Task-specific variances
        
        self.X_train = None
        self.y_train = None  # Shape: (n_samples, num_tasks)
        self.K_inv = None
    
    def fit(self, X: np.ndarray, Y: np.ndarray, optimize_hyperparameters: bool = True):
        """
        Fit Multi-Output GP
        
        Args:
            X: Training inputs (n_samples, n_features)
            Y: Training outputs (n_samples, num_tasks)
            optimize_hyperparameters: Whether to optimize parameters
        """
        self.X_train = X if X.ndim == 2 else X.reshape(-1, 1)
        self.y_train = Y
        
        # Initialize coregionalization parameters
        self._initialize_coregionalization()
        
        if optimize_hyperparameters:
            self._optimize_parameters()
        else:
            self._optimize_coregionalization()
    
    def _initialize_coregionalization(self):
        """Initialize coregionalization matrices"""
        # Initialize B as identity-like matrix
        self.B = np.eye(self.num_tasks, self.num_latent)
        
        # Initialize W as small random values
        self.W = 0.1 * np.random.randn(self.num_tasks, self.num_latent)
        
        # Initialize kappa as ones
        self.kappa = np.ones(self.num_tasks)
    
    def _compute_cross_covariance(self, X1: np.ndarray, X2: np.ndarray) -> np.ndarray:
        """Compute cross-covariance matrix between X1 and X2"""
        K_base = self.kernel.compute(X1, X2)
        
        # Apply coregionalization
        # K = B * K_base * B.T + W * W.T * K_base + diag(kappa) * K_base
        K_cross = np.kron(self.B, K_base)
        
        # Add task-specific components
        for i in range(self.num_tasks):
            for j in range(self.num_tasks):
                if i == j:
                    # Diagonal block
                    K_cross[i::self.num_tasks, j::self.num_tasks] += (
                        self.kappa[i] * K_base + 
                        self.W[i, :].dot(self.W[i, :].T) * K_base
                    )
                else:
                    # Off-diagonal block
                    K_cross[i::self.num_tasks, j::self.num_tasks] += (
                        self.B[i, :].dot(self.B[j, :].T) * K_base
                    )
        
        return K_cross
    
    def _compute_marginal_likelihood(self) -> float:
        """Compute marginal likelihood"""
        # Compute full covariance matrix
        K = self._compute_cross_covariance(self.X_train, self.X_train)
        K += self.kappa * np.eye(len(self.y_train.flatten()))
        
        try:
            # Cholesky decomposition
            L = cholesky(K, lower=True)
            alpha = solve(L.T, solve(L, self.y_train.flatten()))
            
            # Log marginal likelihood
            log_likelihood = -0.5 * (
                self.y_train.flatten().dot(alpha) +
                np.sum(np.log(np.diag(L))) +
                len(self.y_train.flatten()) * np.log(2 * np.pi)
            )
            
            return log_likelihood
        except np.linalg.LinAlgError:
            return -np.inf
    
    def _optimize_coregionalization(self):
        """Optimize coregionalization parameters"""
        def objective(params):
            # Reshape parameters
            B_flat = params[:self.num_tasks * self.num_latent]
            W_flat = params[self.num_tasks * self.num_latent:2 * self.num_tasks * self.num_latent]
            kappa = params[2 * self.num_tasks * self.num_latent:]
            
            self.B = B_flat.reshape(self.num_tasks, self.num_latent)
            self.W = W_flat.reshape(self.num_tasks, self.num_latent)
            self.kappa = kappa
            
            return -self._compute_marginal_likelihood()
        
        # Initial parameters
        initial_params = np.concatenate([
            self.B.flatten(),
            self.W.flatten(),
            self.kappa
        ])
        
        # Optimization bounds
        bounds = [(-10, 10)] * (2 * self.num_tasks * self.num_latent) + [(1e-5, 100)] * self.num_tasks
        
        # Optimize
        result = minimize(
            objective,
            initial_params,
            method='L-BFGS-B',
            bounds=bounds,
            options={'maxiter': 100}
        )
        
        # Update parameters
        optimized_params = result.x
        self.B = optimized_params[:self.num_tasks * self.num_latent].reshape(self.num_tasks, self.num_latent)
        self.W = optimized_params[self.num_tasks * self.num_latent:2 * self.num_tasks * self.num_latent].reshape(self.num_tasks, self.num_latent)
        self.kappa = optimized_params[2 * self.num_tasks * self.num_latent:]
    
    def _optimize_parameters(self):
        """Optimize all parameters including kernel hyperparameters"""
        def objective(params):
            # Split parameters
            n_kernel_params = len(self.kernel.parameters)
            kernel_params = params[:n_kernel_params]
            coregionalization_params = params[n_kernel_params:]
            
            # Set kernel parameters
            for i, param_name in enumerate(self.kernel.parameters.keys()):
                self.kernel.parameters[param_name] = kernel_params[i]
            
            # Set coregionalization parameters
            self.B = coregionalization_params[:self.num_tasks * self.num_latent].reshape(self.num_tasks, self.num_latent)
            self.W = coregionalization_params[self.num_tasks * self.num_latent:2 * self.num_tasks * self.num_latent].reshape(self.num_tasks, self.num_latent)
            self.kappa = coregionalization_params[2 * self.num_tasks * self.num_latent:]
            
            return -self._compute_marginal_likelihood()
        
        # Initial parameters
        kernel_params = list(self.kernel.parameters.values())
        coregionalization_params = np.concatenate([
            self.B.flatten(),
            self.W.flatten(),
            self.kappa
        ])
        initial_params = kernel_params + coregionalization_params.tolist()
        
        # Optimization bounds
        n_kernel = len(kernel_params)
        bounds = [(1e-5, 100)] * n_kernel + [(-10, 10)] * (2 * self.num_tasks * self.num_latent) + [(1e-5, 100)] * self.num_tasks
        
        # Optimize
        result = minimize(
            objective,
            initial_params,
            method='L-BFGS-B',
            bounds=bounds,
            options={'maxiter': 100}
        )
        
        # Update parameters
        optimized_params = result.x
        for i, param_name in enumerate(self.kernel.parameters.keys()):
            self.kernel.parameters[param_name] = optimized_params[i]
        
        self.B = optimized_params[n_kernel:n_kernel + self.num_tasks * self.num_latent].reshape(self.num_tasks, self.num_latent)
        self.W = optimized_params[n_kernel + self.num_tasks * self.num_latent:n_kernel + 2 * self.num_tasks * self.num_latent].reshape(self.num_tasks, self.num_latent)
        self.kappa = optimized_params[n_kernel + 2 * self.num_tasks * self.num_latent:]
    
    def predict(self, X_test: np.ndarray, return_std: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """Make multi-output predictions"""
        X_test = X_test if X_test.ndim == 2 else X_test.reshape(-1, 1)
        
        # Compute kernel matrices
        K_train_train = self._compute_cross_covariance(self.X_train, self.X_train)
        K_train_test = self._compute_cross_covariance(self.X_train, X_test)
        K_test_test = self._compute_cross_covariance(X_test, X_test)
        
        # Add noise
        K_train_train += self.kappa * np.eye(len(self.y_train.flatten()))
        
        try:
            # Cholesky decomposition
            L = cholesky(K_train_train, lower=True)
            alpha = solve(L.T, solve(L, self.y_train.flatten()))
            
            # Predictive mean
            mean = K_train_test.T.dot(alpha)
            mean = mean.reshape(-1, self.num_tasks)
            
            if return_std:
                # Predictive variance
                v = solve(L, K_train_test)
                var = K_test_test - v.T.dot(v)
                std = np.sqrt(np.maximum(np.diag(var).reshape(-1, self.num_tasks), 1e-10))
                
                return mean, std
            else:
                return mean, None
        except np.linalg.LinAlgError:
            # Fallback to simple prediction
            mean = np.zeros((len(X_test), self.num_tasks))
            std = np.ones((len(X_test), self.num_tasks))
            return mean, std

# Example usage with multi-output GP
def example_multi_output_gp():
    """Example: Multi-Output GP for related tasks"""
    
    # Generate multi-output data
    np.random.seed(42)
    X_train = np.linspace(0, 10, 50)
    
    # Three related tasks
    y1 = np.sin(X_train) + 0.1 * np.random.randn(50)
    y2 = np.cos(X_train) + 0.1 * np.random.randn(50)
    y3 = np.sin(X_train) * np.cos(X_train) + 0.1 * np.random.randn(50)
    
    Y_train = np.column_stack([y1, y2, y3])
    
    # Create multi-output GP
    kernel = RBFKernel(lengthscale=2.0, variance=1.0)
    mogp = MultiOutputGP(kernel, num_tasks=3, num_latent=2)
    
    # Fit multi-output GP
    mogp.fit(X_train, Y_train, optimize_hyperparameters=True)
    
    print("Optimized kernel parameters:")
    for param, value in mogp.kernel.parameters.items():
        print(f"  {param}: {value:.3f}")
    
    print("\nCoregionalization matrices:")
    print("B (task mixing):")
    print(mogp.B)
    print("W (task-specific weights):")
    print(mogp.W)
    print("kappa (task variances):")
    print(mogp.kappa)
    
    # Make predictions
    X_test = np.linspace(-2, 12, 100)
    mean, std = mogp.predict(X_test, return_std=True)
    
    # Plot results
    plt.figure(figsize=(15, 5))
    
    for i in range(3):
        plt.subplot(1, 3, i+1)
        plt.plot(X_train, Y_train[:, i], 'ko', label=f'Task {i+1} data')
        plt.plot(X_test, mean[:, i], 'b-', label=f'Task {i+1} prediction')
        plt.fill_between(X_test, mean[:, i] - 2*std[:, i], mean[:, i] + 2*std[:, i], 
                        alpha=0.3, color='blue')
        plt.title(f'Task {i+1}')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return mogp, X_test, mean, std

if __name__ == "__main__":
    example_multi_output_gp()
```

## Input Format

### Gaussian Process Configuration

```yaml
gaussian_process_config:
  model_type: "standard|sparse|multi_output|deep"
  
  kernel_configuration:
    base_kernel: "rbf|matern|periodic|linear|polynomial"
    kernel_parameters: dict      # Lengthscale, variance, etc.
    composite_kernels: array     # Sum/product of kernels
    automatic_kernel_selection: boolean
    
  training_configuration:
    noise_variance: number       # Observation noise
    optimization_method: "gradient_descent|derivative_free"
    max_iterations: number       # Optimization iterations
    convergence_tolerance: number
    
  sparse_gp_configuration:
    inducing_points: number      # Number of inducing points
    inducing_point_method: "random|kmeans|optimization"
    variational_method: "full_rank|diagonal"
    
  multi_output_configuration:
    num_tasks: number            # Number of output tasks
    num_latent: number           # Number of latent processes
    coregionalization_type: "lmc|icm|convolution"
    
  prediction_configuration:
    return_std: boolean          # Return standard deviations
    return_cov: boolean          # Return full covariance
    confidence_level: number     # Confidence interval level
```

### Advanced Configuration

```yaml
advanced_gp_config:
  deep_gaussian_processes:
    num_layers: number           # Number of GP layers
    layer_kernels: array         # Kernel for each layer
    inter_layer_connections: string # How layers connect
    
  automatic_relevance_determination:
    ard_kernel: boolean          # Use ARD kernel
    feature_importance: boolean  # Compute feature importance
    sparsity_control: number     # Sparsity regularization
    
  uncertainty_quantification:
    epistemic_uncertainty: boolean # Model uncertainty
    aleatoric_uncertainty: boolean # Data uncertainty
    calibration_method: string   # Calibration approach
    
  active_learning:
    acquisition_function: "ei|pi|ucb|entropy"
    batch_size: number           # Number of points to query
    exploration_vs_exploitation: number
```

## Output Format

### GP Model Results

```yaml
gp_model_results:
  optimized_parameters:
    kernel_parameters: dict      # Optimized kernel hyperparameters
    noise_variance: number       # Optimized noise variance
    inducing_points: array       # For sparse GP
    coregionalization_matrices: dict # For multi-output GP
    
  model_performance:
    log_marginal_likelihood: number # Model evidence
    predictive_likelihood: number   # Predictive performance
    cross_validation_score: number  # CV performance
    
  uncertainty_quantification:
    predictive_variance: array   # Pointwise predictive variance
    confidence_intervals: array  # Confidence intervals
    uncertainty_decomposition: dict # Epistemic vs aleatoric
    
  computational_metrics:
    training_time: number        # Time to train model
    prediction_time: number      # Time per prediction
    memory_usage: string         # Memory consumption
```

### Sparse GP Results

```yaml
sparse_gp_results:
  inducing_point_analysis:
    inducing_point_locations: array # Locations of inducing points
    inducing_point_importance: array # Importance of each inducing point
    approximation_quality: number   # Quality of sparse approximation
    
  scalability_metrics:
    complexity_reduction: string     # Complexity improvement
    memory_savings: number          # Memory reduction percentage
    speedup_factor: number          # Training speedup
    
  variational_inference:
    elbo_value: number              # Evidence lower bound
    variational_parameters: dict    # Variational mean and covariance
    convergence_metrics: dict       # Convergence information
```

### Multi-Output GP Results

```yaml
multi_output_gp_results:
  task_relationships:
    task_correlation_matrix: array  # Correlation between tasks
    latent_process_weights: array   # Weights of latent processes
    task_specific_components: dict  # Task-specific variations
    
  multi_task_performance:
    individual_task_performance: dict # Performance per task
    joint_prediction_accuracy: number # Overall multi-task accuracy
    task_transfer_benefit: number     # Benefit from multi-task learning
    
  coregionalization_analysis:
    coregionalization_matrix: array   # B matrix
    task_variance_components: array   # kappa values
    latent_process_contributions: dict # Contribution of each latent process
```

## Configuration Options

### Kernel Types

```yaml
kernel_types:
  rbf_kernel:
    description: "Radial basis function (squared exponential) kernel"
    best_for: ["smooth_functions", "interpolation", "regression"]
    parameters: ["lengthscale", "variance"]
    properties: ["stationary", "infinitely_differentiable"]
    
  matern_kernel:
    description: "Matérn kernel with different smoothness levels"
    best_for: ["less_smooth_functions", "spatial_data", "physical_processes"]
    parameters: ["lengthscale", "variance", "nu"]
    properties: ["stationary", "finite_differentiability"]
    
  periodic_kernel:
    description: "Kernel for periodic functions"
    best_for: ["seasonal_data", "cyclical_patterns", "time_series"]
    parameters: ["lengthscale", "variance", "period"]
    properties: ["stationary", "periodic"]
    
  composite_kernels:
    description: "Sum and product of multiple kernels"
    best_for: ["complex_patterns", "multi_scale_functions", "trend_plus_seasonality"]
    parameters: ["kernel_weights", "individual_parameters"]
    properties: ["flexible", "expressive"]
```

### Sparse Approximation Methods

```yaml
sparse_approximation_methods:
  variational_inducing_points:
    description: "Variational inference with inducing points"
    best_for: ["large_datasets", "scalability", "approximation_quality"]
    complexity: "O(n*m^2)"
    parameters: ["num_inducing_points", "inducing_point_locations"]
    
  deterministic_training_condensation:
    description: "Deterministic approximation method"
    best_for: ["very_large_datasets", "extreme_scalability"]
    complexity: "O(n*m)"
    parameters: ["condensation_points", "approximation_order"]
    
  structured_kernel_interpolation:
    description: "Structured approximation using grid-based interpolation"
    best_for: ["gridded_data", "structured_inputs", "fast_computation"]
    complexity: "O(n*log(n))"
    parameters: ["grid_size", "interpolation_method"]
```

## Error Handling

### Model Specification Errors

```yaml
model_specification_errors:
  invalid_kernel_parameters:
    detection_strategy: "parameter_bounds_checking"
    recovery_strategy: "parameter_clipping"
    max_retries: 1
    fallback_action: "default_parameters"
  
  numerical_instability:
    detection_strategy: "cholesky_decomposition_check"
    recovery_strategy: "jitter_addition"
    max_retries: 3
    fallback_action: "simplified_model"
  
  overfitting:
    detection_strategy: "cross_validation_monitoring"
    recovery_strategy: "regularization_increase"
    max_retries: 2
    fallback_action: "model_complexity_reduction"
```

### Optimization Failures

```yaml
optimization_failures:
  convergence_failure:
    detection_strategy: "gradient_norm_monitoring"
    recovery_strategy: "learning_rate_adjustment"
    max_retries: 3
    fallback_action: "derivative_free_optimization"
  
  local_optima:
    detection_strategy: "multiple_initialization_check"
    recovery_strategy: "restart_with_perturbation"
    max_retries: 2
    fallback_action: "grid_search_initialization"
  
  parameter_drift:
    detection_strategy: "parameter_range_monitoring"
    recovery_strategy: "parameter_regularization"
    max_retries: 2
    fallback_action: "constrained_optimization"
```

## Performance Optimization

### Algorithm Optimization

```python
# Optimization: Structured kernel computations
class StructuredKernel:
    """Kernel with structured computations for efficiency"""
    
    def __init__(self, base_kernel):
        self.base_kernel = base_kernel
    
    def compute_structured(self, X1, X2, structure_type="grid|block"):
        """Compute kernel with structure exploitation"""
        if structure_type == "grid":
            return self._compute_grid_kernel(X1, X2)
        elif structure_type == "block":
            return self._compute_block_kernel(X1, X2)
        else:
            return self.base_kernel.compute(X1, X2)
    
    def _compute_grid_kernel(self, X1, X2):
        """Efficient computation for grid-structured inputs"""
        # Exploit Kronecker structure for grid inputs
        # This can reduce complexity from O(n^2) to O(n^(d/p))
        pass
    
    def _compute_block_kernel(self, X1, X2):
        """Efficient computation for block-structured inputs"""
        # Exploit block structure for faster computation
        pass
```

### Memory Optimization

```yaml
memory_optimization:
  kernel_matrix_compression:
    technique: "low_rank_approximation"
    memory_reduction: "50-90%"
    implementation: "nystrom_method"
    
  incremental_computation:
    technique: "online_learning"
    memory_reduction: "unlimited_data"
    implementation: "sequential_processing"
    
  distributed_computation:
    technique: "parallel_processing"
    memory_reduction: "cluster_scaling"
    implementation: "mpi_implementation"
    
  disk_based_storage:
    technique: "out_of_core_computation"
    memory_reduction: "disk_limited"
    implementation: "memory_mapping"
```

## Integration Examples

### With Active Learning

```python
# Integration with active learning for optimal data selection
class ActiveLearningGP:
    """GP-based active learning framework"""
    
    def __init__(self, gp_model, acquisition_function="expected_improvement"):
        self.gp_model = gp_model
        self.acquisition_function = acquisition_function
    
    def select_next_points(self, candidate_points, batch_size=1):
        """Select next points to evaluate using acquisition function"""
        if self.acquisition_function == "expected_improvement":
            return self._expected_improvement(candidate_points, batch_size)
        elif self.acquisition_function == "probability_improvement":
            return self._probability_improvement(candidate_points, batch_size)
        elif self.acquisition_function == "upper_confidence_bound":
            return self._upper_confidence_bound(candidate_points, batch_size)
    
    def _expected_improvement(self, candidate_points, batch_size):
        """Expected improvement acquisition function"""
        mean, std = self.gp_model.predict(candidate_points)
        
        # Current best
        current_best = np.min(self.gp_model.y_train)
        
        # Expected improvement
        z = (current_best - mean) / (std + 1e-10)
        ei = std * (z * norm.cdf(z) + norm.pdf(z))
        
        # Select top batch_size points
        indices = np.argsort(ei)[-batch_size:]
        return candidate_points[indices]
```

### With Deep Learning

```python
# Integration with deep learning for deep Gaussian processes
class DeepGaussianProcess:
    """Deep Gaussian Process implementation"""
    
    def __init__(self, layer_configs):
        self.layers = []
        for config in layer_configs:
            kernel = self._create_kernel(config['kernel'])
            gp_layer = GaussianProcess(kernel, config['noise_variance'])
            self.layers.append(gp_layer)
    
    def fit(self, X, y):
        """Fit deep GP layer by layer"""
        current_X = X
        
        for i, layer in enumerate(self.layers):
            if i == len(self.layers) - 1:
                # Last layer predicts y
                layer.fit(current_X, y)
            else:
                # Intermediate layers learn latent representations
                layer.fit(current_X, current_X)  # Autoencoder-like
                # Transform data for next layer
                current_X, _ = layer.predict(current_X)
    
    def predict(self, X):
        """Make predictions through all layers"""
        current_X = X
        
        for layer in self.layers[:-1]:
            current_X, _ = layer.predict(current_X)
        
        # Last layer prediction
        return self.layers[-1].predict(current_X)
```

## Best Practices

1. **Kernel Selection**:
   - Start with RBF kernel for smooth functions
   - Use Matérn for less smooth functions
   - Combine kernels for complex patterns
   - Use domain knowledge for kernel design

2. **Hyperparameter Optimization**:
   - Use multiple random restarts to avoid local optima
   - Apply appropriate bounds to prevent numerical issues
   - Monitor convergence and likelihood values
   - Validate with cross-validation

3. **Scalability**:
   - Use sparse approximations for large datasets
   - Choose appropriate number of inducing points
   - Consider structured kernels for specific input patterns
   - Implement parallel processing when possible

4. **Uncertainty Quantification**:
   - Validate uncertainty estimates with calibration plots
   - Distinguish between epistemic and aleatoric uncertainty
   - Use appropriate confidence intervals
   - Monitor uncertainty in extrapolation regions

## Troubleshooting

### Common Issues

1. **Poor Predictions**: Check kernel choice, increase data, optimize hyperparameters
2. **Slow Training**: Use sparse approximations, reduce data size, optimize implementation
3. **Numerical Instability**: Add jitter, check parameter bounds, use Cholesky decomposition
4. **Overfitting**: Increase noise variance, use regularization, apply cross-validation

### Debug Mode

```python
# Debug mode: Enhanced GP debugging
class DebugGaussianProcess:
    """GP with enhanced debugging capabilities"""
    
    def __init__(self, kernel):
        self.kernel = kernel
        self.debug_log = []
        self.convergence_analysis = {}
        self.sensitivity_analysis = {}
    
    def log_training_step(self, step_data):
        """Log detailed training information"""
        self.debug_log.append({
            'iteration': step_data['iteration'],
            'log_likelihood': step_data['log_likelihood'],
            'parameters': step_data['parameters'],
            'gradient_norm': step_data['gradient_norm'],
            'computation_time': step_data['computation_time']
        })
    
    def analyze_kernel_sensitivity(self):
        """Analyze sensitivity to kernel parameters"""
        self.sensitivity_analysis = {
            'parameter_sensitivity': self._compute_parameter_sensitivity(),
            'input_sensitivity': self._compute_input_sensitivity(),
            'kernel_choice_impact': self._analyze_kernel_choice_impact(),
            'uncertainty_calibration': self._analyze_uncertainty_calibration()
        }
        
        return self.sensitivity_analysis
    
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

### Gaussian Process Performance Metrics

```yaml
gaussian_process_metrics:
  predictive_metrics:
    mean_squared_error: number   # MSE on test data
    mean_absolute_error: number  # MAE on test data
    negative_log_likelihood: number # Predictive NLL
    calibration_score: number    # Calibration of uncertainty
    
  model_complexity_metrics:
    effective_parameters: number # Effective number of parameters
    model_evidence: number       # Marginal likelihood
    complexity_penalty: number   # Complexity regularization term
    
  computational_metrics:
    training_complexity: string  # Training time complexity
    prediction_complexity: string # Prediction time complexity
    memory_complexity: string    # Memory usage complexity
    scalability_factor: number   # Scaling with data size
    
  uncertainty_metrics:
    coverage_probability: number # Coverage of confidence intervals
    interval_width: number       # Average width of confidence intervals
    uncertainty_calibration: number # Calibration of predictive uncertainty
```

## Dependencies

- **Core Libraries**: NumPy, SciPy for mathematical operations
- **Optimization**: CVXPY, Pyomo for parameter optimization
- **Machine Learning**: scikit-learn for integration with ML methods
- **Deep Learning**: PyTorch, TensorFlow for deep GP implementations
- **Sparse Computing**: PyTorch Sparse, JAX for efficient sparse operations
- **Visualization**: Matplotlib, Plotly for result visualization

## Version History

- **1.0.0**: Initial release with comprehensive GP frameworks
- **1.1.0**: Added sparse GP approximations and variational inference
- **1.2.0**: Enhanced multi-output GP and coregionalization models
- **1.3.0**: Improved performance optimization and memory management
- **1.4.0**: Added deep Gaussian processes and active learning integration
- **1.5.0**: Enhanced debugging tools and uncertainty quantification

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

Content for ## Constraints involving Gaussian Processes.