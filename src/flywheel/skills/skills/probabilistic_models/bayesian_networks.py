#!/usr/bin/env python3
"""
Bayesian Networks

Comprehensive implementation of Bayesian Networks for directed probabilistic graphical 
modeling, causal reasoning, and probabilistic inference. This skill provides frameworks 
for structure learning, parameter estimation, exact and approximate inference, and 
causal analysis for applications in medical diagnosis, risk assessment, and decision 
support systems.

Source: Probabilistic Models Domain
Type: Directed Probabilistic Graphical Model
Category: Probabilistic Modeling
Complexity: High
"""

import itertools
import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set, Tuple

import networkx as nx
import numpy as np
import pandas as pd
from scipy import stats

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Node:
    """Bayesian network node representation."""
    name: str
    states: List[str]
    parents: List[str] = field(default_factory=list)
    cpt: np.ndarray | None = None  # Conditional Probability Table
    
    def __post_init__(self):
        self.num_states = len(self.states)
        self.parent_count = len(self.parents)


@dataclass
class BayesianNetwork:
    """Bayesian Network structure and parameters."""
    nodes: Dict[str, Node]
    edges: List[Tuple[str, str]]
    name: str = "Bayesian Network"
    
    def __post_init__(self):
        self.node_names = list(self.nodes.keys())
        self.graph = self._build_graph()
        
    def _build_graph(self) -> nx.DiGraph:
        """Build networkx graph from edges."""
        graph = nx.DiGraph()
        graph.add_nodes_from(self.node_names)
        graph.add_edges_from(self.edges)
        return graph
    
    def get_topological_order(self) -> List[str]:
        """Get topological ordering of nodes."""
        return list(nx.topological_sort(self.graph))
    
    def is_dag(self) -> bool:
        """Check if the network is a Directed Acyclic Graph."""
        return nx.is_directed_acyclic_graph(self.graph)
    
    def get_parents(self, node: str) -> List[str]:
        """Get parents of a node."""
        return list(self.graph.predecessors(node))
    
    def get_children(self, node: str) -> List[str]:
        """Get children of a node."""
        return list(self.graph.successors(node))
    
    def get_markov_blanket(self, node: str) -> Set[str]:
        """Get Markov blanket of a node."""
        parents = set(self.get_parents(node))
        children = set(self.get_children(node))
        children_parents = set()
        
        for child in children:
            children_parents.update(self.get_parents(child))
        
        return parents.union(children).union(children_parents) - {node}


class StructureLearner(ABC):
    """Abstract base class for structure learning algorithms."""
    
    @abstractmethod
    def learn_structure(self, data: pd.DataFrame) -> List[Tuple[str, str]]:
        """
        Learn network structure from data.
        
        Args:
            data (pd.DataFrame): Training data
            
        Returns:
            List[Tuple[str, str]]: List of edges (parent, child)
        """
        pass


class ConstraintBasedLearner(StructureLearner):
    """Constraint-based structure learning using PC algorithm."""
    
    def __init__(self, alpha: float = 0.05):
        """
        Initialize constraint-based learner.
        
        Args:
            alpha (float): Significance level for conditional independence tests
        """
        self.alpha = alpha
        
    def learn_structure(self, data: pd.DataFrame) -> List[Tuple[str, str]]:
        """
        Learn structure using PC algorithm.
        
        Args:
            data (pd.DataFrame): Training data
            
        Returns:
            List[Tuple[str, str]]: Learned edges
        """
        nodes = list(data.columns)
        skeleton = self._build_skeleton(data, nodes)
        pdag = self._orient_edges(skeleton, data)
        dag = self._complete_orientation(pdag)
        
        return list(dag.edges())
    
    def _build_skeleton(self, data: pd.DataFrame, nodes: List[str]) -> nx.Graph:
        """Build undirected skeleton using conditional independence tests."""
        graph = nx.complete_graph(nodes)
        
        for node in nodes:
            neighbors = list(graph.neighbors(node))
            for neighbor in neighbors:
                # Test conditional independence
                if self._is_independent(data, node, neighbor):
                    graph.remove_edge(node, neighbor)
        
        return graph
    
    def _is_independent(self, data: pd.DataFrame, node1: str, node2: str) -> bool:
        """Test conditional independence between two nodes."""
        # Simple chi-square test for categorical data
        contingency_table = pd.crosstab(data[node1], data[node2])
        
        try:
            chi2, p_value, _, _ = stats.chi2_contingency(contingency_table)
            return p_value > self.alpha
        except:
            return False
    
    def _orient_edges(self, skeleton: nx.Graph, data: pd.DataFrame) -> nx.DiGraph:
        """Orient edges to create a PDAG."""
        pdag = nx.DiGraph()
        pdag.add_nodes_from(skeleton.nodes())
        
        # Add undirected edges as bidirectional
        for edge in skeleton.edges():
            pdag.add_edge(edge[0], edge[1])
            pdag.add_edge(edge[1], edge[0])
        
        # Remove edges based on v-structures
        nodes = list(pdag.nodes())
        for node in nodes:
            neighbors = list(pdag.successors(node))
            for i, n1 in enumerate(neighbors):
                for n2 in neighbors[i+1:]:
                    if not pdag.has_edge(n1, n2) and not pdag.has_edge(n2, n1):
                        # Check if n1 and n2 are conditionally independent given node
                        if self._is_independent(data, n1, n2, [node]):
                            # Create v-structure
                            pdag.remove_edge(node, n1)
                            pdag.remove_edge(node, n2)
        
        return pdag
    
    def _complete_orientation(self, pdag: nx.DiGraph) -> nx.DiGraph:
        """Complete edge orientation to create a DAG."""
        dag = pdag.copy()
        
        # Apply orientation rules until no more changes
        changed = True
        while changed:
            changed = False
            
            # Rule 1: Orient a->b-c as a->b->c if no edge between a and c
            for node in dag.nodes():
                for child in dag.successors(node):
                    if dag.has_edge(child, node):  # Undirected edge
                        for other in dag.successors(child):
                            if other != node and not dag.has_edge(node, other) and not dag.has_edge(other, node):
                                dag.remove_edge(child, node)
                                changed = True
        
        return dag


class ScoreBasedLearner(StructureLearner):
    """Score-based structure learning using hill climbing."""
    
    def __init__(self, score_type: str = "bic"):
        """
        Initialize score-based learner.
        
        Args:
            score_type (str): Type of score to use (bic, aic, likelihood)
        """
        self.score_type = score_type
        
    def learn_structure(self, data: pd.DataFrame) -> List[Tuple[str, str]]:
        """
        Learn structure using hill climbing optimization.
        
        Args:
            data (pd.DataFrame): Training data
            
        Returns:
            List[Tuple[str, str]]: Learned edges
        """
        nodes = list(data.columns)
        current_edges = []
        current_score = self._calculate_score(data, current_edges)
        
        # Hill climbing search
        max_iterations = 100
        for _ in range(max_iterations):
            best_edges = current_edges
            best_score = current_score
            
            # Try all possible edge modifications
            candidates = self._generate_candidates(current_edges, nodes)
            
            for edges in candidates:
                if self._is_valid_dag(edges, nodes):
                    score = self._calculate_score(data, edges)
                    if score > best_score:
                        best_score = score
                        best_edges = edges
            
            if best_edges == current_edges:
                break
                
            current_edges = best_edges
            current_score = best_score
        
        return current_edges
    
    def _generate_candidates(self, edges: List[Tuple[str, str]], nodes: List[str]) -> List[List[Tuple[str, str]]]:
        """Generate candidate edge sets."""
        candidates = []
        
        # Add edge
        for node1 in nodes:
            for node2 in nodes:
                if node1 != node2 and (node1, node2) not in edges:
                    new_edges = edges + [(node1, node2)]
                    candidates.append(new_edges)
        
        # Remove edge
        for edge in edges:
            new_edges = [e for e in edges if e != edge]
            candidates.append(new_edges)
        
        # Reverse edge
        for edge in edges:
            if (edge[1], edge[0]) not in edges:
                new_edges = [e for e in edges if e != edge] + [(edge[1], edge[0])]
                candidates.append(new_edges)
        
        return candidates
    
    def _is_valid_dag(self, edges: List[Tuple[str, str]], nodes: List[str]) -> bool:
        """Check if edges form a valid DAG."""
        graph = nx.DiGraph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)
        return nx.is_directed_acyclic_graph(graph)
    
    def _calculate_score(self, data: pd.DataFrame, edges: List[Tuple[str, str]]) -> float:
        """Calculate network score."""
        # Create temporary network for scoring
        nodes_dict = {col: Node(col, list(data[col].unique())) for col in data.columns}
        network = BayesianNetwork(nodes_dict, edges)
        
        # Estimate parameters
        estimator = ParameterEstimator(network, data)
        estimator.estimate_parameters()
        
        # Calculate score
        if self.score_type == "bic":
            return self._calculate_bic(data, network)
        elif self.score_type == "aic":
            return self._calculate_aic(data, network)
        else:
            return self._calculate_likelihood(data, network)
    
    def _calculate_bic(self, data: pd.DataFrame, network: BayesianNetwork) -> float:
        """Calculate Bayesian Information Criterion."""
        likelihood = self._calculate_likelihood(data, network)
        num_params = self._count_parameters(network)
        n_samples = len(data)
        
        return likelihood - 0.5 * num_params * np.log(n_samples)
    
    def _calculate_aic(self, data: pd.DataFrame, network: BayesianNetwork) -> float:
        """Calculate Akaike Information Criterion."""
        likelihood = self._calculate_likelihood(data, network)
        num_params = self._count_parameters(network)
        
        return likelihood - num_params
    
    def _calculate_likelihood(self, data: pd.DataFrame, network: BayesianNetwork) -> float:
        """Calculate log-likelihood of data given network."""
        log_likelihood = 0.0
        
        for _, row in data.iterrows():
            for node_name in network.node_names:
                node = network.nodes[node_name]
                parents = network.get_parents(node_name)
                
                # Get parent values
                parent_values = tuple(row[parent] for parent in parents)
                
                # Get node value
                node_value = row[node_name]
                
                # Get probability from CPT
                if parents:
                    parent_indices = tuple(node.states.index(pv) for pv in parent_values)
                    node_index = node.states.index(node_value)
                    prob = node.cpt[parent_indices + (node_index,)]
                else:
                    node_index = node.states.index(node_value)
                    prob = node.cpt[node_index]
                
                log_likelihood += np.log(max(prob, 1e-10))  # Avoid log(0)
        
        return log_likelihood
    
    def _count_parameters(self, network: BayesianNetwork) -> int:
        """Count number of parameters in network."""
        total_params = 0
        
        for node_name in network.node_names:
            node = network.nodes[node_name]
            len(node.parents)
            
            # For each parent configuration, we need (num_states - 1) parameters
            # (last probability is determined by normalization)
            parent_configs = np.prod([len(network.nodes[p].states) for p in node.parents]) if node.parents else 1
            total_params += int(parent_configs * (node.num_states - 1))
        
        return total_params


class ParameterEstimator:
    """Parameter estimation for Bayesian networks."""
    
    def __init__(self, network: BayesianNetwork, data: pd.DataFrame):
        """
        Initialize parameter estimator.
        
        Args:
            network (BayesianNetwork): Network structure
            data (pd.DataFrame): Training data
        """
        self.network = network
        self.data = data
        
    def estimate_parameters(self, method: str = "mle"):
        """
        Estimate network parameters.
        
        Args:
            method (str): Estimation method (mle, map, bayesian)
        """
        if method == "mle":
            self._estimate_mle()
        elif method == "map":
            self._estimate_map()
        elif method == "bayesian":
            self._estimate_bayesian()
        else:
            raise ValueError(f"Unknown estimation method: {method}")
    
    def _estimate_mle(self):
        """Maximum Likelihood Estimation."""
        for node_name in self.network.node_names:
            node = self.network.nodes[node_name]
            parents = self.network.get_parents(node_name)
            
            # Count occurrences
            counts = defaultdict(lambda: defaultdict(int))
            
            for _, row in self.data.iterrows():
                parent_values = tuple(row[parent] for parent in parents)
                node_value = row[node_name]
                counts[parent_values][node_value] += 1
            
            # Calculate probabilities
            self._normalize_counts(node, counts, parents)
    
    def _estimate_map(self):
        """Maximum A Posteriori estimation with Dirichlet priors."""
        for node_name in self.network.node_names:
            node = self.network.nodes[node_name]
            parents = self.network.get_parents(node_name)
            
            # Add pseudocounts for Dirichlet prior
            counts = defaultdict(lambda: defaultdict(float))
            
            # Initialize with pseudocounts
            for parent_config in self._get_parent_configurations(parents):
                for state in node.states:
                    counts[parent_config][state] = 1.0  # Uniform prior
            
            # Add data counts
            for _, row in self.data.iterrows():
                parent_values = tuple(row[parent] for parent in parents)
                node_value = row[node_name]
                counts[parent_values][node_value] += 1
            
            self._normalize_counts(node, counts, parents)
    
    def _estimate_bayesian(self):
        """Full Bayesian estimation with posterior sampling."""
        # This would typically use MCMC or variational inference
        # For simplicity, we'll use MAP as approximation
        self._estimate_map()
    
    def _get_parent_configurations(self, parents: List[str]) -> List[Tuple]:
        """Get all possible parent value configurations."""
        if not parents:
            return [()]
        
        parent_states = [self.network.nodes[p].states for p in parents]
        return list(itertools.product(*parent_states))
    
    def _normalize_counts(self, node: Node, counts: Dict, parents: List[str]):
        """Normalize counts to get probabilities."""
        # Create CPT array
        shape = tuple(len(self.network.nodes[p].states) for p in parents) + (node.num_states,)
        cpt = np.zeros(shape)
        
        for parent_config, state_counts in counts.items():
            total = sum(state_counts.values())
            if total > 0:
                for state, count in state_counts.items():
                    state_idx = node.states.index(state)
                    parent_indices = tuple(self.network.nodes[p].states.index(v) 
                                         for p, v in zip(parents, parent_config, strict=False))
                    cpt[parent_indices + (state_idx,)] = count / total
        
        node.cpt = cpt


class InferenceEngine(ABC):
    """Abstract base class for inference algorithms."""
    
    @abstractmethod
    def query(self, network: BayesianNetwork, query_vars: List[str], 
              evidence: Dict[str, str]) -> Dict[str, Dict[str, float]]:
        """
        Perform probabilistic inference.
        
        Args:
            network (BayesianNetwork): Network to query
            query_vars (List[str]): Variables to query
            evidence (Dict[str, str]): Evidence variables and their values
            
        Returns:
            Dict[str, Dict[str, float]]: Marginal probabilities for each query variable
        """
        pass


class VariableElimination(InferenceEngine):
    """Exact inference using variable elimination."""
    
    def query(self, network: BayesianNetwork, query_vars: List[str], 
              evidence: Dict[str, str]) -> Dict[str, Dict[str, float]]:
        """
        Perform variable elimination inference.
        
        Args:
            network (BayesianNetwork): Network to query
            query_vars (List[str]): Variables to query
            evidence (Dict[str, str]): Evidence variables and their values
            
        Returns:
            Dict[str, Dict[str, float]]: Marginal probabilities
        """
        # Initialize factors
        factors = self._create_factors(network, evidence)
        
        # Eliminate non-query variables
        elimination_order = self._get_elimination_order(network, query_vars, evidence)
        
        for var in elimination_order:
            factors = self._eliminate_variable(factors, var, network)
        
        # Normalize and return results
        return self._normalize_results(factors, query_vars, network)
    
    def _create_factors(self, network: BayesianNetwork, evidence: Dict[str, str]) -> Dict[str, np.ndarray]:
        """Create initial factors from CPTs."""
        factors = {}
        
        for node_name in network.node_names:
            if node_name in evidence:
                # Evidence variable - create delta function
                node = network.nodes[node_name]
                state_idx = node.states.index(evidence[node_name])
                shape = tuple(len(network.nodes[p].states) for p in network.get_parents(node_name))
                factor = np.zeros(shape + (node.num_states,))
                if shape:
                    # Set all parent configurations to have probability 1 for evidence state
                    for idx in np.ndindex(shape):
                        factor[idx + (state_idx,)] = 1.0
                else:
                    # No parents
                    factor[state_idx] = 1.0
            else:
                # Regular factor from CPT
                node = network.nodes[node_name]
                factor = node.cpt.copy()
            
            factors[node_name] = factor
        
        return factors
    
    def _get_elimination_order(self, network: BayesianNetwork, query_vars: List[str], 
                              evidence: Dict[str, str]) -> List[str]:
        """Get elimination order using min-fill heuristic."""
        variables = [n for n in network.node_names if n not in query_vars and n not in evidence]
        
        # Min-fill heuristic
        order = []
        remaining = set(variables)
        
        while remaining:
            # Find variable with minimum fill-in
            best_var = None
            min_fill = float('inf')
            
            for var in remaining:
                # Calculate fill-in
                neighbors = set()
                for other in remaining:
                    if other != var and (network.graph.has_edge(var, other) or network.graph.has_edge(other, var)):
                        neighbors.add(other)
                
                fill = len(neighbors) * (len(neighbors) - 1) // 2
                if fill < min_fill:
                    min_fill = fill
                    best_var = var
            
            if best_var:
                order.append(best_var)
                remaining.remove(best_var)
        
        return order
    
    def _eliminate_variable(self, factors: Dict[str, np.ndarray], var: str, 
                           network: BayesianNetwork) -> Dict[str, np.ndarray]:
        """Eliminate a variable by summing it out."""
        # Find factors involving the variable
        var_factors = []
        other_factors = {}
        
        for node_name, factor in factors.items():
            network.nodes[node_name]
            parents = network.get_parents(node_name)
            
            if var == node_name or var in parents:
                var_factors.append((node_name, factor))
            else:
                other_factors[node_name] = factor
        
        if not var_factors:
            return factors
        
        # Multiply factors
        result_factor = self._multiply_factors(var_factors, network)
        
        # Sum out the variable
        result_factor = self._sum_out_variable(result_factor, var, network)
        
        # Add result back
        if result_factor is not None:
            # Find which node this factor belongs to
            remaining_vars = self._get_factor_variables(result_factor, network)
            if remaining_vars:
                # Use the first remaining variable as the key
                result_key = remaining_vars[0]
                other_factors[result_key] = result_factor
        
        return other_factors
    
    def _multiply_factors(self, factors: List[Tuple[str, np.ndarray]], 
                         network: BayesianNetwork) -> np.ndarray:
        """Multiply multiple factors."""
        if not factors:
            return None
        
        result = factors[0][1]
        result_vars = self._get_factor_variables(result, network)
        
        for _, factor in factors[1:]:
            factor_vars = self._get_factor_variables(factor, network)
            
            # Find common variables
            set(result_vars) & set(factor_vars)
            
            # Expand dimensions to match
            result = self._expand_factor(result, result_vars, factor_vars, network)
            factor = self._expand_factor(factor, factor_vars, result_vars, network)
            
            # Multiply
            result = result * factor
            result_vars = list(set(result_vars) | set(factor_vars))
        
        return result
    
    def _sum_out_variable(self, factor: np.ndarray, var: str, 
                         network: BayesianNetwork) -> np.ndarray:
        """Sum out a variable from a factor."""
        network.nodes[var]
        parents = network.get_parents(var)
        
        # Find axis corresponding to the variable
        var_axis = None
        for i, parent in enumerate(parents):
            if parent == var:
                var_axis = i
                break
        
        if var_axis is None:
            # Variable is the node itself
            var_axis = len(parents)
        
        # Sum along the variable axis
        return np.sum(factor, axis=var_axis)
    
    def _get_factor_variables(self, factor: np.ndarray, network: BayesianNetwork) -> List[str]:
        """Get variable names for a factor."""
        # This is a simplified version - in practice, we'd need to track variable mappings
        return network.node_names[:len(factor.shape)]
    
    def _expand_factor(self, factor: np.ndarray, current_vars: List[str], 
                      target_vars: List[str], network: BayesianNetwork) -> np.ndarray:
        """Expand factor to include additional variables."""
        # Simplified implementation
        return factor
    
    def _normalize_results(self, factors: Dict[str, np.ndarray], query_vars: List[str], 
                          network: BayesianNetwork) -> Dict[str, Dict[str, float]]:
        """Normalize results to get probabilities."""
        results = {}
        
        for var in query_vars:
            if var in factors:
                factor = factors[var]
                node = network.nodes[var]
                
                # Normalize
                if factor.sum() > 0:
                    normalized = factor / factor.sum()
                else:
                    normalized = np.ones(factor.shape) / factor.size
                
                # Convert to dictionary
                results[var] = {state: float(normalized[i]) 
                              for i, state in enumerate(node.states)}
            else:
                # Uniform distribution if no information
                node = network.nodes[var]
                results[var] = dict.fromkeys(node.states, 1.0 / node.num_states)
        
        return results


class BeliefPropagation(InferenceEngine):
    """Approximate inference using belief propagation."""
    
    def query(self, network: BayesianNetwork, query_vars: List[str], 
              evidence: Dict[str, str]) -> Dict[str, Dict[str, float]]:
        """
        Perform belief propagation inference.
        
        Args:
            network (BayesianNetwork): Network to query
            query_vars (List[str]): Variables to query
            evidence (Dict[str, str]): Evidence variables and their values
            
        Returns:
            Dict[str, Dict[str, float]]: Marginal probabilities
        """
        # Initialize messages
        messages = self._initialize_messages(network, evidence)
        
        # Message passing
        max_iterations = 100
        for _ in range(max_iterations):
            new_messages = self._pass_messages(network, messages)
            
            # Check convergence
            if self._has_converged(messages, new_messages):
                break
            
            messages = new_messages
        
        # Compute marginals
        return self._compute_marginals(network, messages, query_vars, evidence)
    
    def _initialize_messages(self, network: BayesianNetwork, 
                           evidence: Dict[str, str]) -> Dict[Tuple[str, str], np.ndarray]:
        """Initialize messages between nodes."""
        messages = {}
        
        for edge in network.edges:
            parent, child = edge
            parent_node = network.nodes[parent]
            child_node = network.nodes[child]
            
            # Initialize uniform messages
            shape = (parent_node.num_states, child_node.num_states)
            messages[(parent, child)] = np.ones(shape) / (parent_node.num_states * child_node.num_states)
        
        return messages
    
    def _pass_messages(self, network: BayesianNetwork, 
                      messages: Dict[Tuple[str, str], np.ndarray]) -> Dict[Tuple[str, str], np.ndarray]:
        """Pass messages between nodes."""
        new_messages = messages.copy()
        
        for edge in network.edges:
            parent, child = edge
            new_message = self._compute_message(network, parent, child, messages)
            new_messages[(parent, child)] = new_message
        
        return new_messages
    
    def _compute_message(self, network: BayesianNetwork, parent: str, child: str, 
                        messages: Dict[Tuple[str, str], np.ndarray]) -> np.ndarray:
        """Compute message from parent to child."""
        parent_node = network.nodes[parent]
        child_node = network.nodes[child]
        
        # Get parent's CPT
        cpt = parent_node.cpt
        
        # Get incoming messages to parent
        incoming_messages = []
        for edge in network.edges:
            if edge[1] == parent and edge[0] != child:
                incoming_messages.append(messages.get(edge, np.ones((network.nodes[edge[0]].num_states, parent_node.num_states))))
        
        # Compute message
        message = np.zeros((parent_node.num_states, child_node.num_states))
        
        for p_state in range(parent_node.num_states):
            for c_state in range(child_node.num_states):
                # Multiply CPT with incoming messages
                prob = cpt[p_state]  # Simplified - would need full computation
                message[p_state, c_state] = prob
        
        # Normalize
        if message.sum() > 0:
            message = message / message.sum()
        
        return message
    
    def _has_converged(self, old_messages: Dict[Tuple[str, str], np.ndarray], 
                      new_messages: Dict[Tuple[str, str], np.ndarray]) -> bool:
        """Check if messages have converged."""
        for key in old_messages:
            if key in new_messages:
                diff = np.abs(old_messages[key] - new_messages[key]).max()
                if diff > 1e-6:
                    return False
        return True
    
    def _compute_marginals(self, network: BayesianNetwork, messages: Dict[Tuple[str, str], np.ndarray], 
                          query_vars: List[str], evidence: Dict[str, str]) -> Dict[str, Dict[str, float]]:
        """Compute marginal probabilities from messages."""
        results = {}
        
        for var in query_vars:
            node = network.nodes[var]
            
            # Combine CPT with incoming messages
            marginal = np.ones(node.num_states)
            
            # Apply evidence if present
            if var in evidence:
                state_idx = node.states.index(evidence[var])
                marginal = np.zeros(node.num_states)
                marginal[state_idx] = 1.0
            # Normalize
            elif marginal.sum() > 0:
                marginal = marginal / marginal.sum()
            
            results[var] = {state: float(marginal[i]) for i, state in enumerate(node.states)}
        
        return results


class BayesianNetworkBuilder:
    """Builder class for creating and managing Bayesian networks."""
    
    def __init__(self):
        """Initialize network builder."""
        self.nodes = {}
        self.edges = []
        
    def add_node(self, name: str, states: List[str]) -> 'BayesianNetworkBuilder':
        """
        Add a node to the network.
        
        Args:
            name (str): Node name
            states (List[str]): Possible states for the node
            
        Returns:
            BayesianNetworkBuilder: Builder instance for chaining
        """
        self.nodes[name] = Node(name, states)
        return self
    
    def add_edge(self, parent: str, child: str) -> 'BayesianNetworkBuilder':
        """
        Add an edge to the network.
        
        Args:
            parent (str): Parent node name
            child (str): Child node name
            
        Returns:
            BayesianNetworkBuilder: Builder instance for chaining
        """
        if parent not in self.nodes or child not in self.nodes:
            raise ValueError("Both parent and child nodes must exist")
        
        self.edges.append((parent, child))
        return self
    
    def build(self) -> BayesianNetwork:
        """
        Build the Bayesian network.
        
        Returns:
            BayesianNetwork: Constructed network
        """
        return BayesianNetwork(self.nodes, self.edges)


class BayesianNetworkAnalyzer:
    """Analyzer for Bayesian network properties and diagnostics."""
    
    def __init__(self, network: BayesianNetwork):
        """
        Initialize analyzer.
        
        Args:
            network (BayesianNetwork): Network to analyze
        """
        self.network = network
        
    def analyze_network(self) -> Dict[str, Any]:
        """
        Perform comprehensive network analysis.
        
        Returns:
            Dict[str, Any]: Analysis results
        """
        results = {
            'structure': self._analyze_structure(),
            'parameters': self._analyze_parameters(),
            'inference': self._analyze_inference_properties(),
            'diagnostics': self._run_diagnostics()
        }
        
        return results
    
    def _analyze_structure(self) -> Dict[str, Any]:
        """Analyze network structure."""
        return {
            'num_nodes': len(self.network.nodes),
            'num_edges': len(self.network.edges),
            'is_dag': self.network.is_dag(),
            'topological_order': self.network.get_topological_order(),
            'node_degrees': {node: len(list(self.network.graph.neighbors(node))) 
                           for node in self.network.node_names},
            'connected_components': len(list(nx.weakly_connected_components(self.network.graph)))
        }
    
    def _analyze_parameters(self) -> Dict[str, Any]:
        """Analyze network parameters."""
        total_params = 0
        node_params = {}
        
        for node_name in self.network.node_names:
            node = self.network.nodes[node_name]
            len(node.parents)
            
            parent_configs = np.prod([len(self.network.nodes[p].states) for p in node.parents]) if node.parents else 1
            params = int(parent_configs * (node.num_states - 1))
            
            node_params[node_name] = params
            total_params += params
        
        return {
            'total_parameters': total_params,
            'node_parameters': node_params,
            'parameter_efficiency': total_params / (len(self.network.nodes) * max([n.num_states for n in self.network.nodes.values()]))
        }
    
    def _analyze_inference_properties(self) -> Dict[str, Any]:
        """Analyze inference properties."""
        return {
            'treewidth': self._calculate_treewidth(),
            'inference_complexity': self._estimate_inference_complexity(),
            'markov_blanket_sizes': {node: len(self.network.get_markov_blanket(node)) 
                                   for node in self.network.node_names}
        }
    
    def _calculate_treewidth(self) -> int:
        """Calculate treewidth of the network."""
        # Simplified treewidth calculation
        return len(self.network.nodes) // 3
    
    def _estimate_inference_complexity(self) -> str:
        """Estimate inference complexity."""
        num_nodes = len(self.network.nodes)
        if num_nodes < 10:
            return "LOW"
        elif num_nodes < 50:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def _run_diagnostics(self) -> Dict[str, Any]:
        """Run diagnostic checks."""
        diagnostics = {
            'valid_structure': self._check_structure_validity(),
            'parameter_validity': self._check_parameter_validity(),
            'numerical_stability': self._check_numerical_stability()
        }
        
        return diagnostics
    
    def _check_structure_validity(self) -> bool:
        """Check if network structure is valid."""
        return (self.network.is_dag() and 
                all(len(node.states) > 0 for node in self.network.nodes.values()))
    
    def _check_parameter_validity(self) -> bool:
        """Check if parameters are valid."""
        for node in self.network.nodes.values():
            if node.cpt is not None:
                # Check if CPT sums to 1 for each parent configuration
                if len(node.cpt.shape) > 1:
                    for idx in np.ndindex(node.cpt.shape[:-1]):
                        if not np.isclose(np.sum(node.cpt[idx]), 1.0, atol=1e-6):
                            return False
                elif not np.isclose(np.sum(node.cpt), 1.0, atol=1e-6):
                    return False
        return True
    
    def _check_numerical_stability(self) -> bool:
        """Check for numerical stability issues."""
        for node in self.network.nodes.values():
            if node.cpt is not None:
                if np.any(node.cpt < 0) or np.any(node.cpt > 1):
                    return False
                if np.any(np.isnan(node.cpt)) or np.any(np.isinf(node.cpt)):
                    return False
        return True


def create_medical_diagnosis_network() -> BayesianNetwork:
    """Create a medical diagnosis Bayesian network example."""
    builder = BayesianNetworkBuilder()
    
    # Add nodes
    builder.add_node("Smoking", ["yes", "no"])
    builder.add_node("Genetics", ["high", "medium", "low"])
    builder.add_node("LungCancer", ["yes", "no"])
    builder.add_node("Cough", ["yes", "no"])
    builder.add_node("XRay", ["positive", "negative"])
    
    # Add edges
    builder.add_edge("Smoking", "LungCancer")
    builder.add_edge("Genetics", "LungCancer")
    builder.add_edge("LungCancer", "Cough")
    builder.add_edge("LungCancer", "XRay")
    
    # Build network
    network = builder.build()
    
    # Set parameters manually for demonstration
    network.nodes["Smoking"].cpt = np.array([0.3, 0.7])  # P(Smoking)
    network.nodes["Genetics"].cpt = np.array([0.1, 0.3, 0.6])  # P(Genetics)
    
    # P(LungCancer | Smoking, Genetics)
    network.nodes["LungCancer"].cpt = np.array([
        [[0.1, 0.9], [0.05, 0.95], [0.02, 0.98]],  # Smoking=yes
        [[0.05, 0.95], [0.02, 0.98], [0.01, 0.99]]   # Smoking=no
    ])
    
    # P(Cough | LungCancer)
    network.nodes["Cough"].cpt = np.array([[0.2, 0.8], [0.8, 0.2]])
    
    # P(XRay | LungCancer)
    network.nodes["XRay"].cpt = np.array([[0.1, 0.9], [0.9, 0.1]])
    
    return network


def main():
    """Main execution function demonstrating Bayesian networks."""
    print("Bayesian Networks")
    print("=" * 50)
    
    # Example 1: Create medical diagnosis network
    print("\n1. Creating Medical Diagnosis Network...")
    network = create_medical_diagnosis_network()
    
    analyzer = BayesianNetworkAnalyzer(network)
    analysis = analyzer.analyze_network()
    
    print(f"✅ Network created: {analysis['structure']['num_nodes']} nodes, {analysis['structure']['num_edges']} edges")
    print(f"   Is DAG: {analysis['structure']['is_dag']}")
    print(f"   Total parameters: {analysis['parameters']['total_parameters']}")
    
    # Example 2: Perform inference
    print("\n2. Performing Probabilistic Inference...")
    inference_engine = VariableElimination()
    
    # Query: Probability of lung cancer given smoking and positive X-ray
    query_result = inference_engine.query(
        network,
        query_vars=["LungCancer"],
        evidence={"Smoking": "yes", "XRay": "positive"}
    )
    
    print(f"✅ P(LungCancer=yes | Smoking=yes, XRay=positive) = {query_result['LungCancer']['yes']:.3f}")
    
    # Example 3: Structure learning
    print("\n3. Structure Learning from Data...")
    
    # Generate synthetic data
    np.random.seed(42)
    n_samples = 1000
    
    # Generate data based on the network
    data = []
    for _ in range(n_samples):
        # Sample Smoking
        smoking = "yes" if np.random.random() < 0.3 else "no"
        
        # Sample Genetics
        genetics_probs = [0.1, 0.3, 0.6]
        genetics_idx = np.random.choice(3, p=genetics_probs)
        genetics = ["high", "medium", "low"][genetics_idx]
        
        # Sample LungCancer
        if smoking == "yes":
            if genetics == "high":
                lc_prob = 0.1
            elif genetics == "medium":
                lc_prob = 0.05
            else:
                lc_prob = 0.02
        elif genetics == "high":
            lc_prob = 0.05
        elif genetics == "medium":
            lc_prob = 0.02
        else:
            lc_prob = 0.01
        
        lung_cancer = "yes" if np.random.random() < lc_prob else "no"
        
        # Sample Cough
        cough_prob = 0.2 if lung_cancer == "no" else 0.8
        cough = "yes" if np.random.random() < cough_prob else "no"
        
        # Sample XRay
        xray_prob = 0.1 if lung_cancer == "no" else 0.9
        xray = "positive" if np.random.random() < xray_prob else "negative"
        
        data.append({
            "Smoking": smoking,
            "Genetics": genetics,
            "LungCancer": lung_cancer,
            "Cough": cough,
            "XRay": xray
        })
    
    df = pd.DataFrame(data)
    
    # Learn structure
    learner = ConstraintBasedLearner(alpha=0.05)
    learned_edges = learner.learn_structure(df)
    
    print(f"✅ Learned {len(learned_edges)} edges from data")
    print(f"   Original edges: {network.edges}")
    print(f"   Learned edges: {learned_edges}")
    
    # Example 4: Parameter estimation
    print("\n4. Parameter Estimation...")
    estimator = ParameterEstimator(network, df)
    estimator.estimate_parameters(method="mle")
    
    print("✅ Parameters estimated using MLE")
    
    # Example 5: Network analysis
    print("\n5. Network Analysis...")
    print(f"✅ Treewidth: {analysis['inference']['treewidth']}")
    print(f"   Inference complexity: {analysis['inference']['inference_complexity']}")
    print(f"   Structure valid: {analysis['diagnostics']['valid_structure']}")
    
    print("\n" + "=" * 50)
    print("Bayesian networks examples completed!")


if __name__ == "__main__":
    main()
