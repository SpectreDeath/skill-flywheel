---
Domain: probabilistic_models
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: probabilistic-graphical-models
---



## Description

Automatically designs and implements optimal probabilistic graphical models for complex structured data analysis, including factor graphs, conditional random fields, and structured prediction. This skill provides comprehensive frameworks for model structure learning, parameter estimation, inference algorithms, and applications to computer vision, natural language processing, and bioinformatics.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Factor Graphs**: Implement factor graph representations with efficient message passing algorithms
- **Conditional Random Fields**: Design CRFs for sequence labeling, image segmentation, and structured prediction
- **Structure Learning**: Create algorithms for learning graph structure from data
- **Message Passing**: Implement belief propagation, loopy belief propagation, and tree-reweighted algorithms
- **Parameter Estimation**: Design maximum likelihood, MAP, and regularized parameter learning
- **Structured Prediction**: Handle complex output spaces with dependencies and constraints
- **Scalability**: Implement efficient algorithms for large-scale graphical models

## Usage Examples

### Basic Factor Graph Framework

```python
"""
Basic Factor Graph Framework
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Set, Any, Optional
from dataclasses import dataclass
from collections import defaultdict
import networkx as nx
from scipy.optimize import minimize

@dataclass
class Variable:
    """Factor graph variable"""
    name: str
    domain: List[Any]
    evidence: Any = None
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

@dataclass
class Factor:
    """Factor in factor graph"""
    variables: List[Variable]
    values: np.ndarray  # Factor values for each configuration
    
    def __post_init__(self):
        # Validate dimensions
        expected_shape = tuple(len(var.domain) for var in self.variables)
        if self.values.shape != expected_shape:
            raise ValueError(f"Factor values shape {self.values.shape} doesn't match expected {expected_shape}")

class FactorGraph:
    """Factor graph implementation"""
    
    def __init__(self):
        self.variables: Dict[str, Variable] = {}
        self.factors: List[Factor] = []
        self.graph = nx.Graph()
        
    def add_variable(self, name: str, domain: List[Any], evidence: Any = None):
        """Add variable to factor graph"""
        var = Variable(name=name, domain=domain, evidence=evidence)
        self.variables[name] = var
        self.graph.add_node(var)
    
    def add_factor(self, variables: List[str], values: np.ndarray):
        """Add factor to factor graph"""
        var_objects = [self.variables[name] for name in variables]
        factor = Factor(variables=var_objects, values=values)
        self.factors.append(factor)
        
        # Add edges to graph
        for var in var_objects:
            self.graph.add_edge(factor, var)
    
    def get_neighbors(self, node):
        """Get neighbors of a node in factor graph"""
        return list(self.graph.neighbors(node))
    
    def sum_product_bp(self, max_iterations: int = 100, tolerance: float = 1e-6) -> Dict[str, np.ndarray]:
        """
        Sum-product belief propagation algorithm
        
        Returns:
            marginal_probabilities: Dictionary of marginal probabilities for each variable
        """
        # Initialize messages
        messages = {}
        
        # Initialize messages from factors to variables
        for factor in self.factors:
            for var in factor.variables:
                key = (factor, var)
                message_shape = (len(var.domain),)
                messages[key] = np.ones(message_shape) / len(var.domain)
        
        # Initialize messages from variables to factors
        for var in self.variables.values():
            for factor in self.get_neighbors(var):
                key = (var, factor)
                message_shape = (len(var.domain),)
                messages[key] = np.ones(message_shape) / len(var.domain)
        
        # Iterative message passing
        for iteration in range(max_iterations):
            max_change = 0.0
            
            # Update messages from factors to variables
            for factor in self.factors:
                for target_var in factor.variables:
                    # Compute message from factor to variable
                    message = self._compute_factor_to_variable_message(factor, target_var, messages)
                    
                    # Update message
                    key = (factor, target_var)
                    old_message = messages[key].copy()
                    messages[key] = message
                    
                    # Compute change
                    change = np.max(np.abs(message - old_message))
                    max_change = max(max_change, change)
            
            # Update messages from variables to factors
            for var in self.variables.values():
                for target_factor in self.get_neighbors(var):
                    # Compute message from variable to factor
                    message = self._compute_variable_to_factor_message(var, target_factor, messages)
                    
                    # Update message
                    key = (var, target_factor)
                    old_message = messages[key].copy()
                    messages[key] = message
                    
                    # Compute change
                    change = np.max(np.abs(message - old_message))
                    max_change = max(max_change, change)
            
            # Check convergence
            if max_change < tolerance:
                print(f"Sum-product BP converged after {iteration+1} iterations")
                break
        
        # Compute marginal probabilities
        marginals = {}
        for var_name, var in self.variables.items():
            marginal = np.ones(len(var.domain))
            
            # Multiply all incoming messages
            for factor in self.get_neighbors(var):
                key = (factor, var)
                marginal *= messages[key]
            
            # Normalize
            if np.sum(marginal) > 0:
                marginal /= np.sum(marginal)
            
            marginals[var_name] = marginal
        
        return marginals
    
    def _compute_factor_to_variable_message(self, factor: Factor, target_var: Variable, messages: Dict) -> np.ndarray:
        """Compute message from factor to variable"""
        # Get all variables in factor except target
        other_vars = [var for var in factor.variables if var != target_var]
        
        # Initialize message
        message = np.zeros(len(target_var.domain))
        
        # Sum over all configurations of other variables
        for target_idx, target_value in enumerate(target_var.domain):
            # Create partial assignment for target variable
            assignment = {target_var: target_idx}
            
            # Sum over configurations of other variables
            sum_val = 0.0
            self._sum_over_configurations(factor, other_vars, assignment, messages, sum_val)
            
            message[target_idx] = sum_val
        
        # Normalize message
        if np.sum(message) > 0:
            message /= np.sum(message)
        
        return message
    
    def _sum_over_configurations(self, factor: Factor, remaining_vars: List[Variable], 
                                assignment: Dict[Variable, int], messages: Dict, sum_val: float) -> None:
        """Recursively sum over configurations of remaining variables"""
        if not remaining_vars:
            # Compute factor value for this configuration
            factor_value = self._get_factor_value(factor, assignment)
            
            # Multiply by incoming messages
            for var, idx in assignment.items():
                for neighbor_factor in self.get_neighbors(var):
                    if neighbor_factor != factor:
                        key = (neighbor_factor, var)
                        factor_value *= messages[key][idx]
            
            sum_val += factor_value
            return
        
        # Recurse over next variable
        next_var = remaining_vars[0]
        remaining = remaining_vars[1:]
        
        for idx, value in enumerate(next_var.domain):
            assignment[next_var] = idx
            self._sum_over_configurations(factor, remaining, assignment, messages, sum_val)
    
    def _get_factor_value(self, factor: Factor, assignment: Dict[Variable, int]) -> float:
        """Get factor value for given assignment"""
        indices = []
        for var in factor.variables:
            if var in assignment:
                indices.append(assignment[var])
            else:
                # This shouldn't happen in properly formed calls
                indices.append(0)
        
        return factor.values[tuple(indices)]
    
    def _compute_variable_to_factor_message(self, var: Variable, target_factor: Factor, messages: Dict) -> np.ndarray:
        """Compute message from variable to factor"""
        message = np.ones(len(var.domain))
        
        # Multiply messages from all other factors
        for factor in self.get_neighbors(var):
            if factor != target_factor:
                key = (factor, var)
                message *= messages[key]
        
        # Normalize
        if np.sum(message) > 0:
            message /= np.sum(message)
        
        return message
    
    def max_sum_bp(self, max_iterations: int = 100, tolerance: float = 1e-6) -> Dict[str, Any]:
        """
        Max-sum belief propagation for MAP inference
        
        Returns:
            map_assignment: Maximum a posteriori assignment for each variable
        """
        # Similar to sum-product but with max instead of sum
        # Implementation follows same structure but uses max operations
        
        # Initialize messages
        messages = {}
        
        # Initialize messages from factors to variables
        for factor in self.factors:
            for var in factor.variables:
                key = (factor, var)
                message_shape = (len(var.domain),)
                messages[key] = np.zeros(message_shape)
        
        # Initialize messages from variables to factors
        for var in self.variables.values():
            for factor in self.get_neighbors(var):
                key = (var, factor)
                message_shape = (len(var.domain),)
                messages[key] = np.zeros(message_shape)
        
        # Iterative message passing
        for iteration in range(max_iterations):
            max_change = 0.0
            
            # Update messages from factors to variables (max operation)
            for factor in self.factors:
                for target_var in factor.variables:
                    message = self._compute_factor_to_variable_max_message(factor, target_var, messages)
                    
                    key = (factor, target_var)
                    old_message = messages[key].copy()
                    messages[key] = message
                    
                    change = np.max(np.abs(message - old_message))
                    max_change = max(max_change, change)
            
            # Update messages from variables to factors
            for var in self.variables.values():
                for target_factor in self.get_neighbors(var):
                    message = self._compute_variable_to_factor_message(var, target_factor, messages)
                    
                    key = (var, target_factor)
                    old_message = messages[key].copy()
                    messages[key] = message
                    
                    change = np.max(np.abs(message - old_message))
                    max_change = max(max_change, change)
            
            if max_change < tolerance:
                print(f"Max-sum BP converged after {iteration+1} iterations")
                break
        
        # Compute MAP assignment
        map_assignment = {}
        for var_name, var in self.variables.items():
            # Find most likely value
            best_idx = np.argmax(messages[(list(self.get_neighbors(var))[0], var)])
            map_assignment[var_name] = var.domain[best_idx]
        
        return map_assignment

# Example usage
def example_factor_graph():
    """Example: Factor graph for simple constraint satisfaction"""
    
    # Create factor graph
    fg = FactorGraph()
    
    # Add variables
    fg.add_variable("A", [0, 1])
    fg.add_variable("B", [0, 1])
    fg.add_variable("C", [0, 1])
    
    # Add factors (constraints)
    # Factor 1: A XOR B (exactly one of A or B is true)
    xor_values = np.array([
        [1, 0],  # A=0, B=0 -> 1 (satisfies constraint)
        [0, 1],  # A=0, B=1 -> 0 (violates constraint)
        [0, 1],  # A=1, B=0 -> 0 (violates constraint)
        [1, 0]   # A=1, B=1 -> 1 (satisfies constraint)
    ])
    fg.add_factor(["A", "B"], xor_values)
    
    # Factor 2: B OR C (at least one of B or C is true)
    or_values = np.array([
        [0, 1],  # B=0, C=0 -> 0 (violates constraint)
        [1, 1],  # B=0, C=1 -> 1 (satisfies constraint)
        [1, 1],  # B=1, C=0 -> 1 (satisfies constraint)
        [1, 1]   # B=1, C=1 -> 1 (satisfies constraint)
    ])
    fg.add_factor(["B", "C"], or_values)
    
    # Run belief propagation
    marginals = fg.sum_product_bp()
    print("Marginal probabilities:")
    for var_name, marginal in marginals.items():
        print(f"  {var_name}: {marginal}")
    
    # Run max-sum for MAP inference
    map_assignment = fg.max_sum_bp()
    print("\nMAP assignment:")
    for var_name, value in map_assignment.items():
        print(f"  {var_name}: {value}")
    
    return fg, marginals, map_assignment

if __name__ == "__main__":
    example_factor_graph()
```

### Conditional Random Fields for Sequence Labeling

```python
"""
Conditional Random Fields for Sequence Labeling
"""

import numpy as np
from typing import List, Tuple, Dict, Any, Optional
from scipy.optimize import minimize
from scipy.special import logsumexp

class ConditionalRandomField:
    """Linear-chain Conditional Random Field implementation"""
    
    def __init__(self, num_labels: int, feature_extractor=None):
        """
        Initialize CRF
        
        Args:
            num_labels: Number of possible labels
            feature_extractor: Function to extract features from observations
        """
        self.num_labels = num_labels
        self.feature_extractor = feature_extractor or self._default_feature_extractor
        
        # Parameters
        self.transition_weights = None  # Shape: (num_labels, num_labels)
        self.emission_weights = None    # Shape: (num_labels, num_features)
        self.num_features = None
        
    def _default_feature_extractor(self, observation: Any, position: int) -> np.ndarray:
        """Default feature extractor (one-hot encoding)"""
        # Simple one-hot encoding of observation
        features = np.zeros(self.num_labels)
        if observation < self.num_labels:
            features[observation] = 1.0
        return features
    
    def fit(self, X: List[List[Any]], y: List[List[int]], 
            max_iterations: int = 100, learning_rate: float = 0.01):
        """
        Train CRF using gradient descent
        
        Args:
            X: List of observation sequences
            y: List of label sequences
            max_iterations: Maximum number of training iterations
            learning_rate: Learning rate for gradient descent
        """
        # Extract features and determine dimensions
        self.num_features = len(self.feature_extractor(X[0][0], 0))
        
        # Initialize parameters
        self.transition_weights = np.random.randn(self.num_labels, self.num_labels) * 0.1
        self.emission_weights = np.random.randn(self.num_labels, self.num_features) * 0.1
        
        # Training
        for iteration in range(max_iterations):
            total_loss = 0.0
            total_grad_transition = np.zeros_like(self.transition_weights)
            total_grad_emission = np.zeros_like(self.emission_weights)
            
            for seq_X, seq_y in zip(X, y):
                # Compute gradients for this sequence
                loss, grad_transition, grad_emission = self._compute_sequence_gradients(seq_X, seq_y)
                
                total_loss += loss
                total_grad_transition += grad_transition
                total_grad_emission += grad_emission
            
            # Update parameters
            self.transition_weights -= learning_rate * total_grad_transition / len(X)
            self.emission_weights -= learning_rate * total_grad_emission / len(X)
            
            if iteration % 10 == 0:
                print(f"Iteration {iteration}, Average Loss: {total_loss/len(X):.4f}")
    
    def _compute_sequence_gradients(self, seq_X: List[Any], seq_y: List[int]) -> Tuple[float, np.ndarray, np.ndarray]:
        """Compute loss and gradients for a single sequence"""
        seq_length = len(seq_X)
        
        # Forward pass
        alpha = self._forward_pass(seq_X)
        
        # Compute log-likelihood
        log_likelihood = alpha[-1].sum()  # Log partition function
        
        # True sequence score
        true_score = 0.0
        for t in range(seq_length):
            if t == 0:
                # First position: only emission
                features = self.feature_extractor(seq_X[t], t)
                true_score += self.emission_weights[seq_y[t]].dot(features)
            else:
                # Transition + emission
                features = self.feature_extractor(seq_X[t], t)
                true_score += (self.transition_weights[seq_y[t-1], seq_y[t]] + 
                              self.emission_weights[seq_y[t]].dot(features))
        
        # Loss (negative log-likelihood)
        loss = log_likelihood - true_score
        
        # Backward pass for gradients
        grad_transition = np.zeros_like(self.transition_weights)
        grad_emission = np.zeros_like(self.emission_weights)
        
        # Compute marginal probabilities
        beta = self._backward_pass(seq_X)
        
        # Marginal probabilities for transitions
        for t in range(1, seq_length):
            # Compute transition marginals
            features_t = self.feature_extractor(seq_X[t], t)
            
            # Normalization constant
            Z = logsumexp(alpha[t-1][:, np.newaxis] + self.transition_weights + 
                         self.emission_weights.dot(features_t))
            
            # Transition marginals
            for i in range(self.num_labels):
                for j in range(self.num_labels):
                    marginal = np.exp(alpha[t-1][i] + self.transition_weights[i, j] + 
                                     self.emission_weights[j].dot(features_t) - Z)
                    
                    grad_transition[i, j] += marginal
            
            # Emission marginals
            for j in range(self.num_labels):
                marginal = np.exp(alpha[t][j] + beta[t][j] - log_likelihood)
                grad_emission[j] += marginal * features_t
        
        # Subtract true counts
        for t in range(seq_length):
            if t > 0:
                grad_transition[seq_y[t-1], seq_y[t]] -= 1.0
            grad_emission[seq_y[t]] -= self.feature_extractor(seq_X[t], t)
        
        return loss, grad_transition, grad_emission
    
    def _forward_pass(self, seq_X: List[Any]) -> np.ndarray:
        """Forward pass to compute alpha values"""
        seq_length = len(seq_X)
        alpha = np.zeros((seq_length, self.num_labels))
        
        for t in range(seq_length):
            features = self.feature_extractor(seq_X[t], t)
            
            if t == 0:
                # First position
                alpha[t] = self.emission_weights.dot(features)
            else:
                # Recursion: alpha_t(j) = sum_i alpha_{t-1}(i) * exp(transition(i,j) + emission(j))
                emission_scores = self.emission_weights.dot(features)
                alpha[t] = logsumexp(alpha[t-1][:, np.newaxis] + 
                                   self.transition_weights + emission_scores, axis=0)
        
        return alpha
    
    def _backward_pass(self, seq_X: List[Any]) -> np.ndarray:
        """Backward pass to compute beta values"""
        seq_length = len(seq_X)
        beta = np.zeros((seq_length, self.num_labels))
        
        for t in range(seq_length - 1, -1, -1):
            features = self.feature_extractor(seq_X[t], t)
            
            if t == seq_length - 1:
                # Last position
                beta[t] = 0.0
            else:
                # Recursion: beta_t(i) = sum_j exp(transition(i,j) + emission(j)) * beta_{t+1}(j)
                emission_scores = self.emission_weights.dot(features)
                beta[t] = logsumexp(self.transition_weights + emission_scores[:, np.newaxis] + 
                                  beta[t+1], axis=1)
        
        return beta
    
    def predict(self, seq_X: List[Any]) -> List[int]:
        """Predict most likely label sequence using Viterbi algorithm"""
        seq_length = len(seq_X)
        
        # Viterbi variables
        viterbi = np.zeros((seq_length, self.num_labels))
        backpointers = np.zeros((seq_length, self.num_labels), dtype=int)
        
        # Initialize
        features_0 = self.feature_extractor(seq_X[0], 0)
        viterbi[0] = self.emission_weights.dot(features_0)
        
        # Recursion
        for t in range(1, seq_length):
            features = self.feature_extractor(seq_X[t], t)
            emission_scores = self.emission_weights.dot(features)
            
            for j in range(self.num_labels):
                # Find best previous state
                scores = viterbi[t-1] + self.transition_weights[:, j] + emission_scores[j]
                best_prev = np.argmax(scores)
                
                viterbi[t, j] = scores[best_prev]
                backpointers[t, j] = best_prev
        
        # Termination
        best_last = np.argmax(viterbi[-1])
        
        # Backtrack
        predicted_labels = [0] * seq_length
        predicted_labels[-1] = best_last
        
        for t in range(seq_length - 2, -1, -1):
            predicted_labels[t] = backpointers[t+1, predicted_labels[t+1]]
        
        return predicted_labels
    
    def predict_proba(self, seq_X: List[Any]) -> List[np.ndarray]:
        """Predict probability distribution over labels for each position"""
        seq_length = len(seq_X)
        
        # Forward and backward passes
        alpha = self._forward_pass(seq_X)
        beta = self._backward_pass(seq_X)
        
        # Compute log partition function
        log_Z = alpha[-1].sum()
        
        # Compute probabilities
        probabilities = []
        for t in range(seq_length):
            # Marginal probability for position t
            log_probs = alpha[t] + beta[t] - log_Z
            probs = np.exp(log_probs)
            probabilities.append(probs)
        
        return probabilities

# Example usage with CRF
def example_conditional_random_field():
    """Example: CRF for part-of-speech tagging"""
    
    # Generate synthetic data
    np.random.seed(42)
    
    # States: Noun (0), Verb (1), Adjective (2)
    # Observations: Simple word features
    
    def generate_sequence(length: int):
        """Generate a synthetic word sequence with POS tags"""
        states = [0, 1, 2]  # Noun, Verb, Adjective
        words = ['cat', 'dog', 'big', 'small', 'run', 'jump', 'happy', 'sad']
        
        # Transition probabilities (simplified)
        transitions = np.array([
            [0.5, 0.3, 0.2],  # Noun -> Noun, Verb, Adjective
            [0.4, 0.4, 0.2],  # Verb -> Noun, Verb, Adjective
            [0.3, 0.3, 0.4]   # Adjective -> Noun, Verb, Adjective
        ])
        
        # Generate sequence
        seq_words = []
        seq_tags = []
        
        # Start with random state
        current_state = np.random.choice(len(states))
        
        for _ in range(length):
            # Choose word based on state
            if current_state == 0:  # Noun
                word = np.random.choice(['cat', 'dog'])
            elif current_state == 1:  # Verb
                word = np.random.choice(['run', 'jump'])
            else:  # Adjective
                word = np.random.choice(['big', 'small', 'happy', 'sad'])
            
            seq_words.append(word)
            seq_tags.append(current_state)
            
            # Transition to next state
            current_state = np.random.choice(len(states), p=transitions[current_state])
        
        return seq_words, seq_tags
    
    # Generate training data
    X_train = []
    y_train = []
    
    for _ in range(100):
        words, tags = generate_sequence(5)
        X_train.append(words)
        y_train.append(tags)
    
    # Create and train CRF
    crf = ConditionalRandomField(num_labels=3)
    crf.fit(X_train, y_train, max_iterations=50, learning_rate=0.1)
    
    # Test prediction
    test_words = ['cat', 'run', 'big', 'dog', 'jump']
    predicted_tags = crf.predict(test_words)
    probabilities = crf.predict_proba(test_words)
    
    print("Test sequence:", test_words)
    print("Predicted tags:", predicted_tags)
    print("Tag probabilities:")
    for i, probs in enumerate(probabilities):
        print(f"  Position {i}: Noun={probs[0]:.3f}, Verb={probs[1]:.3f}, Adjective={probs[2]:.3f}")
    
    return crf, test_words, predicted_tags, probabilities

if __name__ == "__main__":
    example_conditional_random_field()
```

### Structure Learning for Graphical Models

```python
"""
Structure Learning for Probabilistic Graphical Models
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Any, Optional
from scipy.stats import chi2_contingency, chi2
import networkx as nx
from itertools import combinations

class StructureLearner:
    """Structure learning for probabilistic graphical models"""
    
    def __init__(self, method: str = "constraint_based", alpha: float = 0.05):
        """
        Initialize structure learner
        
        Args:
            method: Learning method ("constraint_based", "score_based", "hybrid")
            alpha: Significance level for conditional independence tests
        """
        self.method = method
        self.alpha = alpha
        self.graph = None
        self.variables = None
        
    def learn_structure(self, data: pd.DataFrame) -> nx.DiGraph:
        """
        Learn graph structure from data
        
        Args:
            data: Dataset with variables as columns
            
        Returns:
            Learned graph structure
        """
        self.variables = list(data.columns)
        
        if self.method == "constraint_based":
            return self._constraint_based_learning(data)
        elif self.method == "score_based":
            return self._score_based_learning(data)
        elif self.method == "hybrid":
            return self._hybrid_learning(data)
        else:
            raise ValueError(f"Unknown method: {self.method}")
    
    def _constraint_based_learning(self, data: pd.DataFrame) -> nx.DiGraph:
        """Constraint-based structure learning (PC algorithm)"""
        # Start with complete undirected graph
        graph = nx.complete_graph(self.variables)
        
        # Phase 1: Remove edges based on conditional independence
        k = 0
        while True:
            edges_to_remove = []
            
            for edge in list(graph.edges()):
                u, v = edge
                
                # Get neighbors
                neighbors_u = list(graph.neighbors(u))
                if v in neighbors_u:
                    neighbors_u.remove(v)
                
                # Test conditional independence for different conditioning set sizes
                if k <= len(neighbors_u):
                    for subset in combinations(neighbors_u, k):
                        independent = self._test_conditional_independence(data, u, v, set(subset))
                        
                        if independent:
                            edges_to_remove.append((u, v))
                            break
                
                # Also check neighbors of v
                neighbors_v = list(graph.neighbors(v))
                if u in neighbors_v:
                    neighbors_v.remove(u)
                
                if k <= len(neighbors_v):
                    for subset in combinations(neighbors_v, k):
                        independent = self._test_conditional_independence(data, u, v, set(subset))
                        
                        if independent:
                            edges_to_remove.append((u, v))
                            break
            
            # Remove edges
            for edge in edges_to_remove:
                graph.remove_edge(*edge)
            
            # Check if we need to continue
            if k >= len(self.variables) - 2 or not edges_to_remove:
                break
            
            k += 1
        
        # Convert to directed graph
        return self._orient_edges(graph)
    
    def _test_conditional_independence(self, data: pd.DataFrame, X: str, Y: str, Z: set) -> bool:
        """Test conditional independence using chi-square test"""
        if len(Z) == 0:
            # Marginal independence test
            contingency_table = pd.crosstab(data[X], data[Y])
            chi2_stat, p_value, _, _ = chi2_contingency(contingency_table)
        else:
            # Conditional independence test
            grouped = data.groupby(list(Z))
            chi2_stats = []
            dfs = []
            
            for _, group in grouped:
                if len(group) > 1:
                    contingency_table = pd.crosstab(group[X], group[Y])
                    if contingency_table.shape[0] > 1 and contingency_table.shape[1] > 1:
                        chi2_stat, p_val, _, _ = chi2_contingency(contingency_table)
                        chi2_stats.append(chi2_stat)
                        dfs.append((contingency_table.shape[0]-1) * (contingency_table.shape[1]-1))
            
            if chi2_stats:
                chi2_stat = sum(chi2_stats)
                df_total = sum(dfs)
                p_value = 1 - chi2.cdf(chi2_stat, df_total)
            else:
                chi2_stat = 0
                p_value = 1.0
        
        return p_value > self.alpha
    
    def _orient_edges(self, skeleton: nx.Graph) -> nx.DiGraph:
        """Orient edges in the skeleton"""
        dag = nx.DiGraph()
        dag.add_nodes_from(skeleton.nodes())
        dag.add_edges_from(skeleton.edges())
        
        # Apply orientation rules
        changed = True
        while changed:
            changed = False
            
            # Rule 1: If a->b-c and no edge between a,c, then orient b->c
            for a, b in list(dag.edges()):
                if dag.has_edge(b, a):  # Undirected edge
                    for c in dag.neighbors(b):
                        if c != a and not dag.has_edge(a, c) and not dag.has_edge(c, a):
                            if dag.has_edge(c, b):
                                dag.remove_edge(c, b)
                                changed = True
        
        return dag
    
    def _score_based_learning(self, data: pd.DataFrame) -> nx.DiGraph:
        """Score-based structure learning"""
        # Start with empty graph
        best_graph = nx.DiGraph()
        best_graph.add_nodes_from(self.variables)
        
        # Greedy search
        improved = True
        while improved:
            improved = False
            current_score = self._compute_bic_score(data, best_graph)
            
            # Try adding edges
            for u in self.variables:
                for v in self.variables:
                    if u != v and not best_graph.has_edge(u, v):
                        # Add edge
                        test_graph = best_graph.copy()
                        test_graph.add_edge(u, v)
                        
                        # Check for cycles
                        if nx.is_directed_acyclic_graph(test_graph):
                            score = self._compute_bic_score(data, test_graph)
                            
                            if score > current_score:
                                best_graph = test_graph
                                current_score = score
                                improved = True
        
        return best_graph
    
    def _compute_bic_score(self, data: pd.DataFrame, graph: nx.DiGraph) -> float:
        """Compute BIC score for a graph"""
        n_samples = len(data)
        log_likelihood = 0.0
        num_parameters = 0
        
        # Compute log-likelihood and count parameters
        for node in graph.nodes():
            parents = list(graph.predecessors(node))
            
            if not parents:
                # Root node: estimate marginal distribution
                counts = data[node].value_counts()
                probs = counts / len(data)
                log_likelihood += np.sum(counts * np.log(probs + 1e-10))
                num_parameters += len(counts) - 1
            else:
                # Conditional distribution
                parent_values = data[parents].values
                unique_parents, inverse_indices = np.unique(parent_values, axis=0, return_inverse=True)
                
                for i, parent_config in enumerate(unique_parents):
                    mask = inverse_indices == i
                    subset = data[mask]
                    
                    if len(subset) > 0:
                        counts = subset[node].value_counts()
                        probs = counts / len(subset)
                        log_likelihood += np.sum(counts * np.log(probs + 1e-10))
                        num_parameters += len(counts) - 1
        
        # BIC score
        bic = log_likelihood - 0.5 * num_parameters * np.log(n_samples)
        return bic
    
    def _hybrid_learning(self, data: pd.DataFrame) -> nx.DiGraph:
        """Hybrid structure learning (constraint-based + score-based)"""
        # First phase: constraint-based to get skeleton
        skeleton = self._constraint_based_learning(data)
        
        # Second phase: score-based refinement
        return self._score_based_learning(data)

# Example usage with structure learning
def example_structure_learning():
    """Example: Learning structure from synthetic data"""
    
    # Generate synthetic data with known structure
    np.random.seed(42)
    n_samples = 1000
    
    data = []
    for _ in range(n_samples):
        # A -> B -> C, A -> C (diamond structure)
        A = np.random.choice([0, 1], p=[0.5, 0.5])
        
        if A == 0:
            B = np.random.choice([0, 1], p=[0.8, 0.2])
        else:
            B = np.random.choice([0, 1], p=[0.2, 0.8])
        
        if A == 0 and B == 0:
            C = np.random.choice([0, 1], p=[0.9, 0.1])
        elif A == 0 and B == 1:
            C = np.random.choice([0, 1], p=[0.6, 0.4])
        elif A == 1 and B == 0:
            C = np.random.choice([0, 1], p=[0.6, 0.4])
        else:
            C = np.random.choice([0, 1], p=[0.1, 0.9])
        
        data.append({"A": A, "B": B, "C": C})
    
    df = pd.DataFrame(data)
    
    # Learn structure using different methods
    methods = ["constraint_based", "score_based", "hybrid"]
    
    for method in methods:
        learner = StructureLearner(method=method, alpha=0.05)
        learned_graph = learner.learn_structure(df)
        
        print(f"\n{method.upper()} Structure Learning:")
        print("Learned edges:")
        for edge in learned_graph.edges():
            print(f"  {edge[0]} -> {edge[1]}")
    
    # True structure should be: A->B, B->C, A->C
    print("\nTrue Structure:")
    print("  A -> B")
    print("  B -> C") 
    print("  A -> C")
    
    return df

if __name__ == "__main__":
    example_structure_learning()
```

## Input Format

### Probabilistic Graphical Model Configuration

```yaml
probabilistic_graphical_model_config:
  model_type: "factor_graph|conditional_random_field|bayesian_network|markov_random_field"
  
  factor_graph_config:
    variables: array              # List of variable definitions
    factors: array                # List of factor definitions
    inference_algorithm: "sum_product|belief_propagation|loopy_bp"
    
  crf_config:
    num_labels: number            # Number of possible labels
    feature_extractor: string     # Feature extraction method
    regularization: string        # Regularization type
    training_algorithm: "gradient_descent|lbfgs"
    
  structure_learning_config:
    method: "constraint_based|score_based|hybrid"
    significance_level: number    # For constraint-based methods
    scoring_function: "bic|aic|bdeu"
    search_strategy: "greedy|hill_climbing|genetic"
    
  inference_config:
    exact_inference: boolean      # Use exact or approximate inference
    approximation_method: "variational|mcmc|particle_filter"
    convergence_tolerance: number
    max_iterations: number
```

### Advanced Configuration

```yaml
advanced_pgm_config:
  deep_probabilistic_graphical_models:
    neural_network_architecture: string # Architecture for deep PGMs
    parameter_sharing: boolean          # Whether to share parameters
    hierarchical_structure: boolean     # Hierarchical model structure
    
  structured_prediction:
    output_space_structure: string      # Structure of output space
    constraint_handling: string         # How to handle constraints
    loss_function: string               # Loss function for training
    
  scalable_inference:
    distributed_computation: boolean    # Use distributed computing
    parallel_processing: boolean        # Use parallel processing
    memory_optimization: boolean        # Optimize memory usage
    
  uncertainty_quantification:
    epistemic_uncertainty: boolean      # Model uncertainty
    aleatoric_uncertainty: boolean      # Data uncertainty
    uncertainty_propagation: boolean    # Propagate uncertainty through model
```

## Output Format

### Model Structure

```yaml
model_structure:
  variables: array              # List of model variables
  factors: array                # List of model factors
  graph_structure: dict         # Graph representation
  connectivity_analysis: dict   # Analysis of graph connectivity
  
  structural_properties:
    number_of_variables: number
    number_of_factors: number
    graph_diameter: number
    clustering_coefficient: number
    modularity: number
```

### Parameter Estimates

```yaml
parameter_estimates:
  factor_parameters: dict       # Parameters for each factor
  transition_parameters: dict   # Transition probabilities
  emission_parameters: dict     # Emission probabilities
  regularization_parameters: dict # Regularization parameters
  
  parameter_statistics:
    total_parameters: number
    parameters_per_factor: dict
    parameter_uncertainty: dict
    convergence_metrics: dict
```

### Inference Results

```yaml
inference_results:
  marginal_probabilities: dict  # Marginal probabilities for variables
  conditional_probabilities: dict # Conditional probability queries
  most_likely_assignment: dict  # MAP assignment
  partition_function: number    # Normalization constant
  
  inference_performance:
    computation_time: number
    memory_usage: string
    convergence_rate: number
    approximation_error: number
```

### Structure Learning Results

```yaml
structure_learning_results:
  learned_graph: dict           # Learned graph structure
  edge_confidences: dict        # Confidence in learned edges
  structural_similarity: number # Similarity to ground truth
  learning_trajectory: array    # Evolution of structure during learning
  
  model_selection:
    best_model_score: number    # Score of best model
    model_complexity: number    # Complexity of selected model
    cross_validation_scores: array # CV scores for model selection
```

## Configuration Options

### Model Types

```yaml
model_types:
  factor_graphs:
    description: "General factor graph representation"
    best_for: ["constraint_satisfaction", "error_correcting_codes", "image_processing"]
    complexity: "O(exp(tree_width))"
    parameters: ["factor_functions", "variable_domains"]
    
  conditional_random_fields:
    description: "Discriminative model for structured prediction"
    best_for: ["sequence_labeling", "image_segmentation", "natural_language_processing"]
    complexity: "O(sequence_length * num_labels^2)"
    parameters: ["transition_weights", "emission_weights"]
    
  markov_random_fields:
    description: "Undirected graphical model"
    best_for: ["image_analysis", "spatial_modeling", "physics_simulations"]
    complexity: "O(exp(clique_size))"
    parameters: ["potential_functions", "interaction_strengths"]
    
  bayesian_networks:
    description: "Directed acyclic graph representation"
    best_for: ["causal_modeling", "medical_diagnosis", "decision_analysis"]
    complexity: "O(exp(parent_set_size))"
    parameters: ["conditional_probability_tables", "structural_parameters"]
```

### Inference Algorithms

```yaml
inference_algorithms:
  exact_inference:
    belief_propagation:
      description: "Message passing on tree-structured graphs"
      best_for: ["tree_graphs", "sparse_graphs", "exact_computation"]
      complexity: "O(tree_width * exp(tree_width))"
      
    junction_tree:
      description: "Exact inference using tree decomposition"
      best_for: ["moderate_tree_width", "exact_computation", "multiple_queries"]
      complexity: "O(exp(clique_size))"
      
  approximate_inference:
    loopy_belief_propagation:
      description: "Belief propagation on graphs with cycles"
      best_for: ["loopy_graphs", "fast_approximation", "iterative_methods"]
      complexity: "O(iterations * num_edges * exp(max_degree))"
      
    variational_inference:
      description: "Optimization-based approximation"
      best_for: ["large_graphs", "tractable_approximations", "scalability"]
      complexity: "O(iterations * num_variables)"
      
    monte_carlo_methods:
      description: "Sampling-based approximation"
      best_for: ["complex_distributions", "flexible_approximation", "asymptotic_exactness"]
      complexity: "O(samples * mixing_time)"
```

## Error Handling

### Structure Learning Failures

```yaml
structure_learning_failures:
  insufficient_data:
    detection_strategy: "sample_complexity_analysis"
    recovery_strategy: "data_augmentation"
    max_retries: 2
    fallback_action: "simpler_model"
  
  high_dimensionality:
    detection_strategy: "curse_of_dimensionality_check"
    recovery_strategy: "dimensionality_reduction"
    max_retries: 1
    fallback_action: "constraint_based_only"
  
  convergence_failure:
    detection_strategy: "optimization_convergence_monitoring"
    recovery_strategy: "parameter_initialization_restart"
    max_retries: 3
    fallback_action: "heuristic_initialization"
```

### Inference Failures

```yaml
inference_failures:
  computational_intractability:
    detection_strategy: "complexity_estimation"
    recovery_strategy: "approximate_inference"
    max_retries: 1
    fallback_action: "variational_approximation"
  
  numerical_instability:
    detection_strategy: "numerical_range_checking"
    recovery_strategy: "regularization"
    max_retries: 2
    fallback_action: "simplified_model"
  
  convergence_issues:
    detection_strategy: "convergence_monitoring"
    recovery_strategy: "adaptive_parameters"
    max_retries: 2
    fallback_action: "alternative_algorithm"
```

## Performance Optimization

### Algorithm Optimization

```python
# Optimization: Efficient factor graph operations
class OptimizedFactorGraph:
    """Factor graph with optimized operations"""
    
    def __init__(self):
        self.variables = {}
        self.factors = []
        self.variable_to_factors = defaultdict(list)
        
    def add_factor_optimized(self, variables, values):
        """Add factor with optimized indexing"""
        # Use sparse representation for large factors
        if values.size > 1000:
            from scipy.sparse import csr_matrix
            values = csr_matrix(values)
        
        factor = Factor(variables, values)
        self.factors.append(factor)
        
        # Update indexing
        for var in variables:
            self.variable_to_factors[var.name].append(factor)
    
    def compute_marginals_optimized(self):
        """Compute marginals with optimized message passing"""
        # Use efficient data structures
        messages = {}
        
        # Batch message computation
        for factor in self.factors:
            # Compute all messages from this factor at once
            self._batch_compute_factor_messages(factor, messages)
        
        return self._compute_marginals_from_messages(messages)
```

### Memory Optimization

```yaml
memory_optimization:
  factor_compression:
    technique: "tensor_decomposition"
    memory_reduction: "60-90%"
    implementation: "cp_decomposition"
    
  incremental_computation:
    technique: "streaming_algorithms"
    memory_reduction: "unlimited_sequences"
    implementation: "online_learning"
    
  sparse_representations:
    technique: "sparse_matrix_storage"
    memory_reduction: "70-95%"
    implementation: "compressed_sparse_format"
    
  parallel_processing:
    technique: "distributed_computation"
    memory_reduction: "cluster_scaling"
    implementation: "mpi_implementation"
```

## Integration Examples

### With Computer Vision

```python
# Integration with computer vision for image segmentation
class ImageSegmentationCRF:
    """CRF for image segmentation tasks"""
    
    def __init__(self, num_labels, spatial_neighbors=4):
        self.num_labels = num_labels
        self.spatial_neighbors = spatial_neighbors
        
    def extract_image_features(self, image, pixel_position):
        """Extract features for a pixel in an image"""
        row, col = pixel_position
        height, width = image.shape[:2]
        
        # Color features
        if len(image.shape) == 3:
            features = image[row, col, :].flatten()
        else:
            features = np.array([image[row, col]])
        
        # Spatial features
        spatial_features = np.array([row / height, col / width])
        
        # Neighborhood features (if available)
        neighbor_features = []
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)][:self.spatial_neighbors]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < height and 0 <= nc < width:
                if len(image.shape) == 3:
                    neighbor_features.extend(image[nr, nc, :])
                else:
                    neighbor_features.append(image[nr, nc])
        
        return np.concatenate([features, spatial_features, neighbor_features])
    
    def add_spatial_constraints(self, crf_model):
        """Add spatial smoothness constraints to CRF"""
        # Add pairwise potentials for neighboring pixels
        # This encourages neighboring pixels to have similar labels
        pass
```

### With Natural Language Processing

```python
# Integration with NLP for sequence labeling
class NLPSequenceLabeler:
    """CRF for NLP sequence labeling tasks"""
    
    def __init__(self, vocabulary, label_set):
        self.vocabulary = vocabulary
        self.label_set = label_set
        self.crf = ConditionalRandomField(len(label_set))
        
    def extract_text_features(self, tokens, position):
        """Extract features from text tokens"""
        features = []
        
        # Current word features
        word = tokens[position]
        features.append(self.vocabulary.get(word, 0))
        
        # Prefix/suffix features
        if len(word) > 3:
            features.append(hash(word[:3]) % 1000)  # Prefix
            features.append(hash(word[-3:]) % 1000)  # Suffix
        
        # Capitalization features
        features.append(int(word[0].isupper()))
        features.append(int(word.isupper()))
        
        # Previous/next word features
        if position > 0:
            features.append(self.vocabulary.get(tokens[position-1], 0))
        if position < len(tokens) - 1:
            features.append(self.vocabulary.get(tokens[position+1], 0))
        
        return np.array(features)
    
    def train(self, training_data):
        """Train CRF on labeled text data"""
        # training_data: list of (tokens, labels) pairs
        X = []
        y = []
        
        for tokens, labels in training_data:
            X.append([self.extract_text_features(tokens, i) for i in range(len(tokens))])
            y.append([self.label_set.index(label) for label in labels])
        
        self.crf.fit(X, y)
```

## Best Practices

1. **Model Selection**:
   - Choose appropriate model type based on problem structure
   - Use domain knowledge to constrain model complexity
   - Validate model assumptions with data analysis

2. **Parameter Estimation**:
   - Use regularization to prevent overfitting
   - Apply appropriate optimization algorithms
   - Monitor convergence and parameter stability

3. **Inference**:
   - Choose exact vs approximate methods based on graph structure
   - Use efficient algorithms for large-scale problems
   - Validate inference results with known test cases

4. **Structure Learning**:
   - Use appropriate significance levels for constraint-based methods
   - Apply domain constraints to guide structure learning
   - Validate learned structures with domain experts

## Troubleshooting

### Common Issues

1. **Poor Model Fit**: Check model assumptions, increase model complexity, add more data
2. **Slow Inference**: Use approximate methods, optimize graph structure, implement parallel processing
3. **Overfitting**: Apply regularization, use cross-validation, simplify model structure
4. **Convergence Issues**: Adjust optimization parameters, use better initialization, check for multimodality

### Debug Mode

```python
# Debug mode: Enhanced PGM debugging
class DebugProbabilisticGraphicalModel:
    """PGM with enhanced debugging capabilities"""
    
    def __init__(self, model_type):
        self.model_type = model_type
        self.debug_log = []
        self.convergence_analysis = {}
        self.structure_analysis = {}
    
    def log_inference_step(self, step_data):
        """Log detailed inference information"""
        self.debug_log.append({
            'step': step_data['step'],
            'variables_processed': step_data['variables_processed'],
            'computation_time': step_data['computation_time'],
            'memory_usage': step_data['memory_usage'],
            'approximation_error': step_data.get('approximation_error', 0.0)
        })
    
    def analyze_graph_structure(self):
        """Analyze graph structure and properties"""
        self.structure_analysis = {
            'connectivity': self._analyze_connectivity(),
            'treewidth': self._compute_treewidth(),
            'bottlenecks': self._identify_bottlenecks(),
            'convergence_patterns': self._analyze_convergence_patterns()
        }
        
        return self.structure_analysis
    
    def generate_debug_report(self):
        """Generate comprehensive debug report"""
        return {
            'structure_analysis': self.analyze_graph_structure(),
            'inference_analysis': self.analyze_inference_performance(),
            'parameter_analysis': self.analyze_parameter_estimates(),
            'recommendations': self.get_optimization_recommendations()
        }
```

## Monitoring and Metrics

### Probabilistic Graphical Model Performance Metrics

```yaml
probabilistic_graphical_model_metrics:
  structural_metrics:
    structural_similarity: number # Similarity to ground truth
    edge_precision: number        # Precision of learned edges
    edge_recall: number           # Recall of learned edges
    f1_score: number              # Harmonic mean of precision and recall
    
  parameter_metrics:
    parameter_accuracy: number    # Accuracy of parameter estimates
    log_likelihood: number        # Log-likelihood of data
    bic_score: number             # Bayesian Information Criterion
    aic_score: number             # Akaike Information Criterion
    
  inference_metrics:
    inference_accuracy: number    # Accuracy of inference results
    computation_time: number      # Time for inference
    memory_efficiency: number     # Memory usage efficiency
    approximation_quality: number # Quality of approximate methods
    
  predictive_metrics:
    prediction_accuracy: number   # Accuracy of predictions
    calibration_score: number     # Calibration of probability estimates
    sharpness_score: number       # Sharpness of predictions
    brier_score: number           # Brier score for probabilistic predictions
```

## Dependencies

- **Core Libraries**: NumPy, SciPy for mathematical operations
- **Graph Libraries**: NetworkX for graph operations and structure analysis
- **Optimization**: CVXPY, Pyomo for parameter optimization
- **Machine Learning**: scikit-learn for integration with ML methods
- **Probabilistic Programming**: PyMC3, Stan for advanced Bayesian modeling
- **Visualization**: Matplotlib, Plotly for network and result visualization

## Version History

- **1.0.0**: Initial release with comprehensive PGM frameworks
- **1.1.0**: Added factor graphs and advanced CRF implementations
- **1.2.0**: Enhanced structure learning algorithms and optimization
- **1.3.0**: Improved performance optimization and memory management
- **1.4.0**: Added deep probabilistic graphical models and scalable inference
- **1.5.0**: Enhanced debugging tools and model validation techniques

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

To be provided dynamically during execution.