---
Domain: probabilistic_models
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: bayesian-networks
---



## Description

Automatically designs and implements optimal Bayesian networks for probabilistic reasoning, causal inference, and uncertainty quantification. This skill provides comprehensive frameworks for structure learning, parameter estimation, inference algorithms, and model validation in complex probabilistic systems.


## Purpose

*[Content for Purpose section to be added based on the specific skill requirements]*

## Examples

*[Content for Examples section to be added based on the specific skill requirements]*

## Implementation Notes

*[Content for Implementation Notes section to be added based on the specific skill requirements]*
## Capabilities

- **Structure Learning**: Implement constraint-based, score-based, and hybrid algorithms for network topology discovery
- **Parameter Estimation**: Design maximum likelihood, Bayesian, and EM-based parameter learning methods
- **Inference Algorithms**: Create exact inference (variable elimination, junction trees) and approximate inference (MCMC, variational)
- **Causal Analysis**: Implement causal discovery, intervention modeling, and counterfactual reasoning
- **Model Validation**: Design cross-validation, goodness-of-fit tests, and model comparison techniques
- **Dynamic Models**: Extend to dynamic Bayesian networks and hidden Markov models
- **Scalability**: Implement efficient algorithms for large-scale networks with thousands of variables

## Usage Examples

### Basic Bayesian Network Framework

```python
"""
Basic Bayesian Network Framework
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Set, Any, Optional
from dataclasses import dataclass
from collections import defaultdict
import networkx as nx
from scipy.stats import chi2_contingency
from sklearn.preprocessing import LabelEncoder

@dataclass
class Node:
    """Bayesian network node representation"""
    name: str
    states: List[str]
    parents: List[str] = None
    cpt: np.ndarray = None  # Conditional Probability Table
    
    def __post_init__(self):
        if self.parents is None:
            self.parents = []
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.name == other.name

class BayesianNetwork:
    """Basic Bayesian Network implementation"""
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.graph = nx.DiGraph()
        self.data: Optional[pd.DataFrame] = None
        
    def add_node(self, name: str, states: List[str], parents: List[str] = None):
        """Add node to the network"""
        if parents is None:
            parents = []
        
        # Validate parents exist
        for parent in parents:
            if parent not in self.nodes:
                raise ValueError(f"Parent node '{parent}' not found")
        
        node = Node(name=name, states=states, parents=parents)
        self.nodes[name] = node
        self.graph.add_node(name)
        
        # Add edges
        for parent in parents:
            self.graph.add_edge(parent, name)
    
    def estimate_parameters(self, data: pd.DataFrame):
        """Estimate parameters using maximum likelihood"""
        self.data = data
        
        for node_name, node in self.nodes.items():
            # Get parent values for indexing
            parent_values = []
            for parent in node.parents:
                parent_values.append(data[parent].values)
            
            # Count occurrences
            if len(node.parents) == 0:
                # Root node - simple frequency
                counts = data[node_name].value_counts()
                total = len(data)
                probabilities = counts / total
                node.cpt = probabilities.reindex(node.states, fill_value=0.0).values
            else:
                # Conditional probability table
                parent_combinations = list(set(zip(*parent_values)))
                cpt_shape = [len(node.states)] + [len(self.nodes[p].states) for p in node.parents]
                cpt = np.zeros(cpt_shape)
                
                for i, combination in enumerate(parent_combinations):
                    # Filter data for this parent combination
                    mask = True
                    for j, (parent, value) in enumerate(zip(node.parents, combination)):
                        mask = mask & (data[parent] == value)
                    
                    subset = data[mask]
                    if len(subset) > 0:
                        # Count child states
                        state_counts = subset[node_name].value_counts()
                        total_count = len(subset)
                        
                        for k, state in enumerate(node.states):
                            count = state_counts.get(state, 0)
                            # Calculate indices for CPT
                            indices = [k] + [self.nodes[p].states.index(combination[j]) 
                                            for j, p in enumerate(node.parents)]
                            cpt[tuple(indices)] = count / total_count
                
                # Normalize to ensure probabilities sum to 1
                for indices in np.ndindex(cpt_shape[1:]):
                    slice_idx = tuple([slice(None)] + list(indices))
                    row_sum = np.sum(cpt[slice_idx])
                    if row_sum > 0:
                        cpt[slice_idx] /= row_sum
                
                node.cpt = cpt
    
    def query(self, query_vars: List[str], evidence: Dict[str, str] = None) -> Dict[str, float]:
        """Perform exact inference using variable elimination"""
        if evidence is None:
            evidence = {}
        
        # Initialize factors
        factors = []
        for node_name, node in self.nodes.items():
            # Create factor for this node
            if node_name in evidence:
                # Evidence variable - create delta function
                evidence_idx = node.states.index(evidence[node_name])
                factor_shape = [len(self.nodes[p].states) for p in node.parents]
                factor = np.zeros(factor_shape + [len(node.states)])
                
                if len(factor_shape) == 0:
                    factor[evidence_idx] = 1.0
                else:
                    # Set evidence state to 1, others to 0
                    for indices in np.ndindex(factor_shape):
                        factor[tuple(list(indices) + [evidence_idx])] = 1.0
                
                factors.append((node_name, factor))
            else:
                # Regular factor
                factors.append((node_name, node.cpt))
        
        # Variable elimination
        remaining_vars = set(self.nodes.keys()) - set(query_vars) - set(evidence.keys())
        
        while remaining_vars:
            # Pick variable to eliminate (heuristic: minimum fill-in)
            var_to_eliminate = min(remaining_vars, key=lambda v: self._get_elimination_cost(v, factors))
            remaining_vars.remove(var_to_eliminate)
            
            # Find factors containing this variable
            var_factors = [f for f in factors if var_to_eliminate in f[0]]
            other_factors = [f for f in factors if var_to_eliminate not in f[0]]
            
            if var_factors:
                # Multiply factors
                result_factor = self._multiply_factors(var_factors)
                
                # Sum out the variable
                result_factor = self._sum_out_variable(result_factor, var_to_eliminate)
                
                other_factors.append((var_to_eliminate, result_factor))
            
            factors = other_factors
        
        # Multiply remaining factors
        if factors:
            result = factors[0][1]
            for _, factor in factors[1:]:
                result = self._multiply_factors([(None, result), (None, factor)])
        else:
            result = np.array([1.0])
        
        # Normalize
        if result.sum() > 0:
            result = result / result.sum()
        
        # Extract query results
        results = {}
        for i, state in enumerate(query_vars[0].states if len(query_vars) == 1 else self.nodes[query_vars[0]].states):
            results[state] = result[i] if len(result.shape) == 1 else result[i].sum()
        
        return results
    
    def _get_elimination_cost(self, var: str, factors: List[Tuple[str, np.ndarray]]) -> int:
        """Calculate elimination cost for variable"""
        # Count variables that will be connected after elimination
        connected_vars = set()
        for factor_name, factor in factors:
            if var in factor_name:
                connected_vars.update(factor_name)
        connected_vars.discard(var)
        return len(connected_vars)
    
    def _multiply_factors(self, factors: List[Tuple[str, np.ndarray]]) -> np.ndarray:
        """Multiply multiple factors"""
        if not factors:
            return np.array([1.0])
        
        result = factors[0][1]
        result_vars = set(factors[0][0]) if isinstance(factors[0][0], str) else set(factors[0][0])
        
        for factor_name, factor in factors[1:]:
            # Align dimensions
            factor_vars = set(factor_name) if isinstance(factor_name, str) else set(factor_name)
            
            # Find common variables
            common_vars = result_vars.intersection(factor_vars)
            
            # Reshape factors to align dimensions
            # This is a simplified implementation - full version would handle arbitrary dimension ordering
            result = np.outer(result.flatten(), factor.flatten()).reshape(result.shape + factor.shape)
            
            result_vars = result_vars.union(factor_vars)
        
        return result
    
    def _sum_out_variable(self, factor: np.ndarray, variable: str) -> np.ndarray:
        """Sum out a variable from a factor"""
        # Find axis corresponding to variable
        # Simplified implementation - assumes variable is last dimension
        return np.sum(factor, axis=-1)

# Example usage
def example_basic_bayesian_network():
    """Example: Basic Bayesian Network for medical diagnosis"""
    
    # Create network
    bn = BayesianNetwork()
    
    # Add nodes
    bn.add_node("Smoking", ["yes", "no"])
    bn.add_node("LungCancer", ["yes", "no"], ["Smoking"])
    bn.add_node("Cough", ["yes", "no"], ["LungCancer"])
    bn.add_node("XRay", ["positive", "negative"], ["LungCancer"])
    
    # Create sample data
    np.random.seed(42)
    n_samples = 1000
    
    data = []
    for _ in range(n_samples):
        # Smoking
        smoking = "yes" if np.random.random() < 0.3 else "no"
        
        # Lung cancer depends on smoking
        if smoking == "yes":
            lung_cancer = "yes" if np.random.random() < 0.2 else "no"
        else:
            lung_cancer = "yes" if np.random.random() < 0.05 else "no"
        
        # Cough depends on lung cancer
        if lung_cancer == "yes":
            cough = "yes" if np.random.random() < 0.8 else "no"
        else:
            cough = "yes" if np.random.random() < 0.1 else "no"
        
        # X-ray depends on lung cancer
        if lung_cancer == "yes":
            xray = "positive" if np.random.random() < 0.9 else "negative"
        else:
            xray = "positive" if np.random.random() < 0.1 else "negative"
        
        data.append({
            "Smoking": smoking,
            "LungCancer": lung_cancer,
            "Cough": cough,
            "XRay": xray
        })
    
    df = pd.DataFrame(data)
    
    # Estimate parameters
    bn.estimate_parameters(df)
    
    # Perform queries
    print("Query: P(LungCancer | Smoking=yes)")
    result1 = bn.query(["LungCancer"], {"Smoking": "yes"})
    print(f"  P(LungCancer=yes) = {result1['yes']:.3f}")
    print(f"  P(LungCancer=no) = {result1['no']:.3f}")
    
    print("\nQuery: P(LungCancer | Cough=yes, XRay=positive)")
    result2 = bn.query(["LungCancer"], {"Cough": "yes", "XRay": "positive"})
    print(f"  P(LungCancer=yes) = {result2['yes']:.3f}")
    print(f"  P(LungCancer=no) = {result2['no']:.3f}")
    
    return bn, df

if __name__ == "__main__":
    example_basic_bayesian_network()
```

### Advanced Structure Learning with Constraint-Based Methods

```python
"""
Advanced Structure Learning using Constraint-Based Methods
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Set, Tuple, Any
from scipy.stats import chi2_contingency, chi2
import networkx as nx
from itertools import combinations

class ConstraintBasedStructureLearning:
    """PC Algorithm for constraint-based structure learning"""
    
    def __init__(self, alpha: float = 0.05):
        """
        Initialize PC algorithm
        
        Args:
            alpha: Significance level for conditional independence tests
        """
        self.alpha = alpha
        self.skeleton = None
        self.sepsets = {}
        
    def conditional_independence_test(self, X: str, Y: str, Z: Set[str], data: pd.DataFrame) -> Tuple[bool, float]:
        """
        Test conditional independence using chi-square test
        
        Args:
            X, Y: Variables to test
            Z: Conditioning set
            data: Dataset
            
        Returns:
            (independent, p_value)
        """
        if len(Z) == 0:
            # Marginal independence test
            contingency_table = pd.crosstab(data[X], data[Y])
            chi2_stat, p_value, _, _ = chi2_contingency(contingency_table)
        else:
            # Conditional independence test
            # Group by conditioning variables
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
        
        return p_value > self.alpha, p_value
    
    def learn_skeleton(self, variables: List[str], data: pd.DataFrame) -> nx.Graph:
        """
        Learn undirected skeleton using PC algorithm
        
        Args:
            variables: List of variable names
            data: Dataset
            
        Returns:
            Undirected graph skeleton
        """
        # Initialize complete undirected graph
        skeleton = nx.Graph()
        skeleton.add_nodes_from(variables)
        
        # Add all possible edges
        for i, var1 in enumerate(variables):
            for var2 in variables[i+1:]:
                skeleton.add_edge(var1, var2)
        
        # Phase 1: Remove edges based on conditional independence
        k = 0
        while True:
            edges_to_remove = []
            for edge in list(skeleton.edges()):
                u, v = edge
                
                # Get neighbors of u (excluding v)
                neighbors_u = list(skeleton.neighbors(u))
                if v in neighbors_u:
                    neighbors_u.remove(v)
                
                # Test conditional independence for different conditioning set sizes
                if k <= len(neighbors_u):
                    for subset in combinations(neighbors_u, k):
                        independent, p_value = self.conditional_independence_test(u, v, set(subset), data)
                        
                        if independent:
                            edges_to_remove.append((u, v))
                            self.sepsets[(u, v)] = set(subset)
                            self.sepsets[(v, u)] = set(subset)
                            break
                
                # Also check neighbors of v
                neighbors_v = list(skeleton.neighbors(v))
                if u in neighbors_v:
                    neighbors_v.remove(u)
                
                if k <= len(neighbors_v):
                    for subset in combinations(neighbors_v, k):
                        independent, p_value = self.conditional_independence_test(u, v, set(subset), data)
                        
                        if independent:
                            edges_to_remove.append((u, v))
                            self.sepsets[(u, v)] = set(subset)
                            self.sepsets[(v, u)] = set(subset)
                            break
            
            # Remove edges
            for edge in edges_to_remove:
                skeleton.remove_edge(*edge)
            
            # Check if we need to continue
            if k >= len(variables) - 2 or not edges_to_remove:
                break
            
            k += 1
        
        return skeleton
    
    def orient_edges(self, skeleton: nx.Graph, variables: List[str]) -> nx.DiGraph:
        """
        Orient edges to create a DAG
        
        Args:
            skeleton: Undirected graph skeleton
            variables: List of variable names
            
        Returns:
            Directed acyclic graph
        """
        dag = nx.DiGraph()
        dag.add_nodes_from(variables)
        dag.add_edges_from(skeleton.edges())
        
        # Phase 2: Orient v-structures
        for node in variables:
            neighbors = list(skeleton.neighbors(node))
            for i, u in enumerate(neighbors):
                for v in neighbors[i+1:]:
                    # Check if u-node-v is a v-structure
                    if not skeleton.has_edge(u, v):
                        # Check if node is not in sepset(u,v)
                        if node not in self.sepsets.get((u, v), set()):
                            # Orient u -> node <- v
                            if dag.has_edge(node, u):
                                dag.remove_edge(node, u)
                            if dag.has_edge(node, v):
                                dag.remove_edge(node, v)
        
        # Phase 3: Apply orientation rules
        changed = True
        while changed:
            changed = False
            
            # Rule 1: If a->b-c and no edge between a,c, then orient b->c
            for a, b in list(dag.edges()):
                if dag.has_edge(b, a):  # Undirected edge
                    for c in dag.neighbors(b):
                        if c != a and not dag.has_edge(a, c) and not dag.has_edge(c, a):
                            # Orient b->c
                            if dag.has_edge(c, b):
                                dag.remove_edge(c, b)
                                changed = True
            
            # Rule 2: If a->b->c and a-c, then orient a->c
            for a in variables:
                for b in dag.successors(a):
                    for c in dag.successors(b):
                        if dag.has_edge(c, a) or dag.has_edge(a, c):
                            # Orient a->c
                            if dag.has_edge(c, a):
                                dag.remove_edge(c, a)
                                changed = True
        
        return dag
    
    def learn_structure(self, data: pd.DataFrame) -> nx.DiGraph:
        """
        Learn Bayesian network structure using PC algorithm
        
        Args:
            data: Dataset with variables as columns
            
        Returns:
            Directed acyclic graph representing the network structure
        """
        variables = list(data.columns)
        
        # Learn skeleton
        self.skeleton = self.learn_skeleton(variables, data)
        
        # Orient edges
        dag = self.orient_edges(self.skeleton, variables)
        
        return dag

# Example usage with structure learning
def example_structure_learning():
    """Example: Learning structure from data"""
    
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
    
    # Learn structure
    pc = ConstraintBasedStructureLearning(alpha=0.05)
    learned_structure = pc.learn_structure(df)
    
    print("Learned Structure:")
    for edge in learned_structure.edges():
        print(f"  {edge[0]} -> {edge[1]}")
    
    # True structure should be: A->B, B->C, A->C
    print("\nTrue Structure:")
    print("  A -> B")
    print("  B -> C") 
    print("  A -> C")
    
    return learned_structure, df

if __name__ == "__main__":
    example_structure_learning()
```

### Variational Inference for Approximate Inference

```python
"""
Variational Inference for Approximate Bayesian Network Inference
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from scipy.optimize import minimize
from scipy.special import softmax
import networkx as nx

class VariationalInference:
    """Variational inference for Bayesian networks"""
    
    def __init__(self, bn_structure: nx.DiGraph, data: pd.DataFrame):
        """
        Initialize variational inference
        
        Args:
            bn_structure: Bayesian network structure
            data: Observed data
        """
        self.structure = bn_structure
        self.data = data
        self.variables = list(data.columns)
        self.variational_params = {}
        
    def initialize_variational_params(self):
        """Initialize variational parameters"""
        for var in self.variables:
            # Initialize as uniform distribution
            num_states = len(self.data[var].unique())
            self.variational_params[var] = np.ones(num_states) / num_states
    
    def compute_elbo(self, params: np.ndarray) -> float:
        """
        Compute Evidence Lower Bound (ELBO)
        
        Args:
            params: Flattened variational parameters
            
        Returns:
            ELBO value
        """
        # Reshape parameters
        self._reshape_params(params)
        
        elbo = 0.0
        
        # Compute expected log likelihood
        for _, row in self.data.iterrows():
            for var in self.variables:
                # Get parent values
                parents = list(self.structure.predecessors(var))
                parent_values = tuple(row[parent] for parent in parents)
                
                # Get current state
                current_state = row[var]
                
                # Add log probability contribution
                if parents:
                    # Conditional probability
                    parent_idx = self._get_parent_index(parents, parent_values)
                    prob = self.variational_params[var][current_state]
                else:
                    # Marginal probability
                    prob = self.variational_params[var][current_state]
                
                if prob > 0:
                    elbo += np.log(prob)
        
        # Subtract KL divergence term
        for var in self.variables:
            # KL(q||p) where p is uniform prior
            uniform_prior = np.ones_like(self.variational_params[var]) / len(self.variational_params[var])
            kl_div = np.sum(self.variational_params[var] * np.log(self.variational_params[var] / uniform_prior))
            elbo -= kl_div
        
        return -elbo  # Return negative for minimization
    
    def _reshape_params(self, params: np.ndarray):
        """Reshape flattened parameters"""
        idx = 0
        for var in self.variables:
            num_states = len(self.variational_params[var])
            self.variational_params[var] = params[idx:idx+num_states]
            # Normalize to ensure it's a valid distribution
            self.variational_params[var] = softmax(self.variational_params[var])
            idx += num_states
    
    def _get_parent_index(self, parents: List[str], parent_values: Tuple) -> int:
        """Get index for parent combination"""
        # Simple encoding - in practice would use proper indexing
        return hash(parent_values) % 1000
    
    def optimize_variational_params(self, max_iter: int = 1000) -> Dict[str, np.ndarray]:
        """
        Optimize variational parameters using gradient descent
        
        Args:
            max_iter: Maximum number of iterations
            
        Returns:
            Optimized variational parameters
        """
        self.initialize_variational_params()
        
        # Flatten parameters for optimization
        initial_params = np.concatenate([self.variational_params[var] for var in self.variables])
        
        # Optimize
        result = minimize(
            self.compute_elbo,
            initial_params,
            method='L-BFGS-B',
            options={'maxiter': max_iter, 'disp': False}
        )
        
        # Reshape optimized parameters
        self._reshape_params(result.x)
        
        return self.variational_params
    
    def query_variational(self, query_vars: List[str], evidence: Dict[str, int] = None) -> Dict[str, float]:
        """
        Perform variational inference query
        
        Args:
            query_vars: Variables to query
            evidence: Evidence variables and their values
            
        Returns:
            Query results
        """
        if evidence is None:
            evidence = {}
        
        results = {}
        for var in query_vars:
            if var in evidence:
                # Evidence variable
                results[var] = {str(evidence[var]): 1.0}
            else:
                # Query variable - use variational distribution
                dist = self.variational_params[var]
                results[var] = {str(i): prob for i, prob in enumerate(dist)}
        
        return results

# Example usage with variational inference
def example_variational_inference():
    """Example: Variational inference for complex Bayesian network"""
    
    # Create complex network structure
    structure = nx.DiGraph()
    structure.add_edges_from([
        ('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('C', 'E'), ('D', 'F')
    ])
    
    # Generate synthetic data
    np.random.seed(42)
    n_samples = 500
    
    data = []
    for _ in range(n_samples):
        A = np.random.choice([0, 1], p=[0.5, 0.5])
        
        if A == 0:
            B = np.random.choice([0, 1], p=[0.8, 0.2])
            C = np.random.choice([0, 1], p=[0.7, 0.3])
        else:
            B = np.random.choice([0, 1], p=[0.2, 0.8])
            C = np.random.choice([0, 1], p=[0.3, 0.7])
        
        # D depends on B and C
        if B == 0 and C == 0:
            D = np.random.choice([0, 1], p=[0.9, 0.1])
        elif B == 0 and C == 1:
            D = np.random.choice([0, 1], p=[0.6, 0.4])
        elif B == 1 and C == 0:
            D = np.random.choice([0, 1], p=[0.6, 0.4])
        else:
            D = np.random.choice([0, 1], p=[0.1, 0.9])
        
        # E depends on C
        if C == 0:
            E = np.random.choice([0, 1], p=[0.8, 0.2])
        else:
            E = np.random.choice([0, 1], p=[0.2, 0.8])
        
        # F depends on D
        if D == 0:
            F = np.random.choice([0, 1], p=[0.9, 0.1])
        else:
            F = np.random.choice([0, 1], p=[0.1, 0.9])
        
        data.append({"A": A, "B": B, "C": C, "D": D, "E": E, "F": F})
    
    df = pd.DataFrame(data)
    
    # Perform variational inference
    vi = VariationalInference(structure, df)
    optimized_params = vi.optimize_variational_params()
    
    # Perform queries
    print("Variational Inference Results:")
    print("Query: P(F | A=1, E=0)")
    result = vi.query_variational(['F'], {'A': 1, 'E': 0})
    print(f"  P(F=0) = {result['F']['0']:.3f}")
    print(f"  P(F=1) = {result['F']['1']:.3f}")
    
    return optimized_params, df

if __name__ == "__main__":
    example_variational_inference()
```

## Input Format

### Bayesian Network Configuration

```yaml
bayesian_network_config:
  structure_definition:
    nodes: array                 # List of node names
    edges: array                 # List of (parent, child) tuples
    node_properties:
      states: dict               # Node -> list of possible states
      type: "discrete|continuous"
      
  parameter_estimation:
    method: "maximum_likelihood|bayesian|em"
    prior_type: "uniform|dirichlet|gaussian"
    hyperparameters: dict        # Prior parameters
    
  inference_configuration:
    algorithm: "exact|variational|mcmc"
    exact_method: "variable_elimination|junction_tree"
    variational_method: "mean_field|structured"
    mcmc_method: "gibbs|metropolis_hastings"
    
  structure_learning:
    method: "constraint_based|score_based|hybrid"
    constraint_method: "pc|ges"
    score_method: "bic|aic|bdeu"
    significance_level: number   # For constraint-based methods
    
  validation:
    cross_validation_folds: number
    test_size: number
    metrics: array               # List of evaluation metrics
```

### Dynamic Bayesian Network Configuration

```yaml
dynamic_bayesian_network_config:
  temporal_structure:
    time_slices: number          # Number of time slices
    intra_slice_edges: array     # Edges within time slice
    inter_slice_edges: array     # Edges between time slices
    
  state_space:
    hidden_states: array         # Hidden state variables
    observed_states: array       # Observed variables
    state_dimensions: dict       # Variable -> dimension
    
  transition_model:
    transition_matrix: array     # State transition probabilities
    emission_matrix: array       # Observation probabilities
    initial_distribution: array  # Initial state probabilities
    
  learning_parameters:
    learning_rate: number        # For parameter updates
    convergence_threshold: number
    max_iterations: number
```

## Output Format

### Network Structure

```yaml
network_structure:
  nodes: array                   # List of node names
  edges: array                   # List of (parent, child) tuples
  adjacency_matrix: array        # Adjacency matrix representation
  topological_order: array       # Topological ordering of nodes
  
  structural_properties:
    number_of_nodes: number
    number_of_edges: number
    maximum_in_degree: number
    maximum_out_degree: number
    connected_components: number
    cycles: boolean              # Whether network contains cycles
    
  complexity_metrics:
    treewidth: number            # Treewidth of the moralized graph
    clique_size: number          # Maximum clique size
    inference_complexity: string # Complexity class
```

### Parameter Estimates

```yaml
parameter_estimates:
  conditional_probability_tables: dict
    node_name:
      parents: array             # List of parent variables
      cpt: array                 # Conditional probability table
      confidence_intervals: array # Parameter uncertainty
      
  parameter_statistics:
    total_parameters: number     # Total number of parameters
    parameters_per_node: dict    # Node -> parameter count
    sparsity_ratio: number       # Ratio of zero parameters
    
  learning_convergence:
    convergence_iteration: number
    final_likelihood: number
    parameter_stability: number  # Measure of parameter stability
```

### Inference Results

```yaml
inference_results:
  query_results: dict            # Query variable -> probability distribution
  marginal_probabilities: dict   # All variables marginal probabilities
  conditional_probabilities: dict # Conditional probability queries
  
  inference_performance:
    computation_time: number     # Time taken for inference
    memory_usage: string         # Memory used during inference
    approximation_error: number  # Error for approximate methods
    
  convergence_analysis:
    convergence_rate: number     # Rate of convergence
    mixing_time: number          # For MCMC methods
    effective_sample_size: number # For sampling methods
```

### Model Validation

```yaml
model_validation:
  cross_validation_results:
    fold_scores: array           # Scores for each fold
    mean_score: number           # Average cross-validation score
    std_score: number            # Standard deviation of scores
    
  goodness_of_fit:
    likelihood_score: number     # Log-likelihood of data
    bic_score: number            # Bayesian Information Criterion
    aic_score: number            # Akaike Information Criterion
    
  predictive_performance:
    accuracy: number             # Prediction accuracy
    precision: number            # Precision of predictions
    recall: number               # Recall of predictions
    f1_score: number             # F1 score
    
  structural_validation:
    structural_similarity: number # Similarity to ground truth structure
    edge_precision: number       # Precision of learned edges
    edge_recall: number          # Recall of learned edges
```

## Configuration Options

### Structure Learning Strategies

```yaml
structure_learning_strategies:
  constraint_based:
    description: "Learn structure using conditional independence tests"
    best_for: ["large_networks", "sparse_structures", "causal_discovery"]
    complexity: "O(n^k * m)"     # n=variables, k=max_conditioning_set_size, m=samples
    parameters: ["significance_level", "max_conditioning_set_size"]
    
  score_based:
    description: "Search for structure that maximizes scoring function"
    best_for: ["smaller_networks", "dense_structures", "optimal_scoring"]
    complexity: "O(n! * m)"      # In worst case, but heuristics reduce this
    parameters: ["scoring_function", "search_strategy", "regularization"]
    
  hybrid:
    description: "Combine constraint-based and score-based approaches"
    best_for: ["medium_networks", "balanced_approach", "robustness"]
    complexity: "O(n^k * m + n^2 * search_complexity)"
    parameters: ["constraint_threshold", "score_threshold", "hybrid_strategy"]
```

### Inference Algorithms

```yaml
inference_algorithms:
  exact_inference:
    variable_elimination:
      description: "Systematically eliminate variables to compute marginals"
      best_for: ["small_networks", "tree_structures", "exact_computation"]
      complexity: "O(exp(treewidth))"
      memory: "O(exp(treewidth))"
      
    junction_tree:
      description: "Convert network to junction tree for efficient inference"
      best_for: ["medium_networks", "multiple_queries", "tree_decompositions"]
      complexity: "O(exp(clique_size))"
      memory: "O(exp(clique_size))"
      
  approximate_inference:
    variational_inference:
      description: "Approximate posterior with tractable distribution"
      best_for: ["large_networks", "fast_approximation", "scalability"]
      complexity: "O(iterations * network_size)"
      accuracy: "Lower bounds on log-likelihood"
      
    mcmc_sampling:
      description: "Generate samples from posterior distribution"
      best_for: ["complex_distributions", "high_accuracy", "flexibility"]
      complexity: "O(samples * mixing_time)"
      accuracy: "Asymptotically_exact"
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
# Optimization: Efficient CPT storage and computation
class OptimizedCPT:
    """Optimized Conditional Probability Table implementation"""
    
    def __init__(self, node_states: List[str], parent_states: Dict[str, List[str]]):
        self.node_states = node_states
        self.parent_states = parent_states
        
        # Use sparse representation for large tables
        self.sparse_cpt = {}
        self.normalization_cache = {}
    
    def get_probability(self, child_state: str, parent_values: Dict[str, str]) -> float:
        """Get probability with caching and sparse lookup"""
        key = (child_state, tuple(sorted(parent_values.items())))
        
        if key in self.sparse_cpt:
            return self.sparse_cpt[key]
        
        # Compute if not cached
        prob = self._compute_probability(child_state, parent_values)
        self.sparse_cpt[key] = prob
        return prob
    
    def _compute_probability(self, child_state: str, parent_values: Dict[str, str]) -> float:
        """Compute probability using optimized algorithms"""
        # Implementation depends on specific probability model
        # Could use interpolation, approximation, or exact computation
        pass
```

### Memory Optimization

```yaml
memory_optimization:
  sparse_representation:
    technique: "sparse_matrix_storage"
    memory_reduction: "60-90%"
    implementation: "compressed_sparse_row"
    
  incremental_computation:
    technique: "lazy_evaluation"
    memory_reduction: "40-70%"
    implementation: "on_demand_calculation"
    
  caching_strategies:
    technique: "lru_caching"
    memory_reduction: "30-50%"
    implementation: "memoization_with_eviction"
    
  parallel_processing:
    technique: "distributed_computation"
    memory_reduction: "unlimited_scaling"
    implementation: "cluster_computing"
```

## Integration Examples

### With Machine Learning

```python
# Integration with machine learning for parameter learning
class MLBayesianNetwork:
    """Bayesian network with machine learning parameter estimation"""
    
    def __init__(self, structure: nx.DiGraph):
        self.structure = structure
        self.ml_models = {}
    
    def learn_parameters_with_ml(self, data: pd.DataFrame, ml_algorithm: str = "random_forest"):
        """Learn parameters using machine learning algorithms"""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        
        for node in self.structure.nodes():
            parents = list(self.structure.predecessors(node))
            
            if not parents:
                # Root node - learn marginal distribution
                self.ml_models[node] = self._learn_marginal(data[node])
            else:
                # Conditional distribution - use ML to learn mapping
                X = data[parents]
                y = data[node]
                
                if ml_algorithm == "random_forest":
                    model = RandomForestClassifier()
                elif ml_algorithm == "logistic_regression":
                    model = LogisticRegression()
                
                model.fit(X, y)
                self.ml_models[node] = model
    
    def _learn_marginal(self, data: pd.Series):
        """Learn marginal distribution using ML"""
        # Could use density estimation, clustering, etc.
        return data.value_counts(normalize=True)
```

### With Causal Inference

```python
# Integration with causal inference
class CausalBayesianNetwork:
    """Bayesian network with causal inference capabilities"""
    
    def __init__(self, structure: nx.DiGraph):
        self.structure = structure
        self.intervention_effects = {}
    
    def do_intervention(self, variable: str, value: Any):
        """Perform do-calculus intervention"""
        # Remove incoming edges to the intervened variable
        parents = list(self.structure.predecessors(variable))
        for parent in parents:
            self.structure.remove_edge(parent, variable)
        
        # Set the variable to the specified value
        self.intervention_effects[variable] = value
    
    def estimate_causal_effect(self, treatment: str, outcome: str, data: pd.DataFrame) -> float:
        """Estimate causal effect using do-calculus"""
        # Implement backdoor adjustment, frontdoor adjustment, etc.
        # This is a simplified version
        return self._compute_adjusted_probability(treatment, outcome, data)
```

## Best Practices

1. **Structure Learning**:
   - Start with domain knowledge to constrain search space
   - Use appropriate significance levels for conditional independence tests
   - Validate learned structure with domain experts

2. **Parameter Estimation**:
   - Handle missing data appropriately (EM algorithm, imputation)
   - Use informative priors when data is sparse
   - Regularize to prevent overfitting

3. **Inference**:
   - Choose exact vs approximate methods based on network size
   - Monitor convergence for iterative algorithms
   - Validate results with known test cases

4. **Model Validation**:
   - Use cross-validation for parameter tuning
   - Compare multiple model structures
   - Validate predictions on held-out data

## Troubleshooting

### Common Issues

1. **Poor Structure Learning**: Increase sample size, adjust significance level, use domain constraints
2. **Slow Inference**: Use approximate methods, optimize variable ordering, reduce network size
3. **Overfitting**: Use regularization, cross-validation, simpler structures
4. **Convergence Issues**: Adjust learning rates, use better initialization, check for multimodality

### Debug Mode

```python
# Debug mode: Enhanced Bayesian network debugging
class DebugBayesianNetwork:
    """Bayesian network with enhanced debugging capabilities"""
    
    def __init__(self, structure: nx.DiGraph):
        self.structure = structure
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
    
    def analyze_structure_complexity(self):
        """Analyze structural complexity and bottlenecks"""
        self.structure_analysis = {
            'treewidth': self._compute_treewidth(),
            'bottleneck_nodes': self._find_bottleneck_nodes(),
            'convergence_patterns': self._analyze_convergence_patterns(),
            'memory_hotspots': self._identify_memory_hotspots()
        }
        
        return self.structure_analysis
    
    def generate_debug_report(self):
        """Generate comprehensive debug report"""
        return {
            'structure_analysis': self.analyze_structure_complexity(),
            'inference_analysis': self.analyze_inference_performance(),
            'parameter_analysis': self.analyze_parameter_estimates(),
            'recommendations': self.get_optimization_recommendations()
        }
```

## Monitoring and Metrics

### Bayesian Network Performance Metrics

```yaml
bayesian_network_metrics:
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
- **Machine Learning**: scikit-learn, PyTorch for ML-based parameter learning
- **Probabilistic Programming**: PyMC3, Stan for advanced Bayesian modeling
- **Visualization**: Matplotlib, Plotly for network and result visualization

## Version History

- **1.0.0**: Initial release with comprehensive Bayesian network frameworks
- **1.1.0**: Added constraint-based structure learning (PC algorithm)
- **1.2.0**: Enhanced variational inference and MCMC methods
- **1.3.0**: Improved performance optimization and memory management
- **1.4.0**: Added dynamic Bayesian networks and causal inference
- **1.5.0**: Enhanced debugging tools and model validation techniques

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

Content for ## Constraints involving Bayesian Networks.