---
Domain: probabilistic_models
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: markov-models
---



## Description

Automatically designs and implements optimal Markov models for sequential data analysis, time series prediction, and state-based modeling. This skill provides comprehensive frameworks for discrete and continuous Markov chains, hidden Markov models, Markov decision processes, and advanced variants with efficient algorithms for parameter estimation, inference, and prediction.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Markov Chain Analysis**: Implement discrete and continuous-time Markov chains with transition matrix analysis
- **Hidden Markov Models**: Design HMMs with forward-backward algorithms, Viterbi decoding, and Baum-Welch training
- **Markov Decision Processes**: Create MDPs with value iteration, policy iteration, and Q-learning algorithms
- **State Estimation**: Implement Kalman filters, particle filters, and sequential Monte Carlo methods
- **Model Selection**: Design criteria for model order selection and structure learning
- **Temporal Analysis**: Analyze mixing times, stationary distributions, and convergence properties
- **Scalability**: Implement efficient algorithms for large state spaces and long sequences

## Usage Examples

### Basic Markov Chain Framework

```python
"""
Basic Markov Chain Framework
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Set, Any, Optional
from dataclasses import dataclass
from collections import defaultdict
import networkx as nx
from scipy.linalg import eig

@dataclass
class MarkovChain:
    """Discrete-time Markov chain implementation"""
    
    states: List[str]
    transition_matrix: np.ndarray
    initial_distribution: np.ndarray = None
    
    def __post_init__(self):
        # Validate transition matrix
        if self.transition_matrix.shape != (len(self.states), len(self.states)):
            raise ValueError("Transition matrix dimensions must match number of states")
        
        # Check if rows sum to 1
        row_sums = np.sum(self.transition_matrix, axis=1)
        if not np.allclose(row_sums, 1.0):
            raise ValueError("Transition matrix rows must sum to 1")
        
        # Set initial distribution if not provided
        if self.initial_distribution is None:
            self.initial_distribution = np.ones(len(self.states)) / len(self.states)
    
    def simulate(self, n_steps: int, start_state: str = None) -> List[str]:
        """Simulate Markov chain for n steps"""
        if start_state is None:
            # Choose initial state based on initial distribution
            start_idx = np.random.choice(len(self.states), p=self.initial_distribution)
        else:
            start_idx = self.states.index(start_state)
        
        current_state = start_idx
        path = [self.states[current_state]]
        
        for _ in range(n_steps - 1):
            # Sample next state
            next_state = np.random.choice(
                len(self.states), 
                p=self.transition_matrix[current_state]
            )
            path.append(self.states[next_state])
            current_state = next_state
        
        return path
    
    def get_stationary_distribution(self) -> np.ndarray:
        """Compute stationary distribution using eigenvalue decomposition"""
        # Find eigenvector corresponding to eigenvalue 1
        eigenvalues, eigenvectors = eig(self.transition_matrix.T)
        
        # Find index of eigenvalue closest to 1
        idx = np.argmin(np.abs(eigenvalues - 1.0))
        
        # Get corresponding eigenvector
        stationary = np.real(eigenvectors[:, idx])
        
        # Normalize to ensure it's a probability distribution
        stationary = stationary / np.sum(stationary)
        
        return stationary
    
    def get_n_step_transition(self, n: int) -> np.ndarray:
        """Compute n-step transition matrix"""
        return np.linalg.matrix_power(self.transition_matrix, n)
    
    def get_hitting_time(self, target_state: str) -> Dict[str, float]:
        """Compute expected hitting times to target state"""
        target_idx = self.states.index(target_state)
        
        # Set up system of linear equations
        # E[i] = 1 + sum_j P[i,j] * E[j] for i != target
        # E[target] = 0
        
        n_states = len(self.states)
        A = np.zeros((n_states, n_states))
        b = np.ones(n_states)
        
        for i in range(n_states):
            if i == target_idx:
                A[i, i] = 1.0
                b[i] = 0.0
            else:
                A[i, i] = 1.0
                for j in range(n_states):
                    if j != target_idx:
                        A[i, j] -= self.transition_matrix[i, j]
        
        hitting_times = np.linalg.solve(A, b)
        return {state: time for state, time in zip(self.states, hitting_times)}
    
    def analyze_communication_classes(self) -> Dict[str, List[str]]:
        """Analyze communication classes and recurrence properties"""
        # Build directed graph
        G = nx.DiGraph()
        G.add_nodes_from(self.states)
        
        # Add edges where transition probability > 0
        for i, state_i in enumerate(self.states):
            for j, state_j in enumerate(self.states):
                if self.transition_matrix[i, j] > 1e-10:
                    G.add_edge(state_i, state_j)
        
        # Find strongly connected components
        scc = list(nx.strongly_connected_components(G))
        
        # Classify states
        communication_classes = {}
        for i, component in enumerate(scc):
            class_name = f"Class_{i+1}"
            communication_classes[class_name] = list(component)
        
        return communication_classes

# Example usage
def example_markov_chain():
    """Example: Weather Markov Chain"""
    
    # Define states
    states = ["Sunny", "Cloudy", "Rainy"]
    
    # Define transition matrix
    # P[i,j] = probability of going from state i to state j
    transition_matrix = np.array([
        [0.7, 0.2, 0.1],  # Sunny -> Sunny, Cloudy, Rainy
        [0.3, 0.4, 0.3],  # Cloudy -> Sunny, Cloudy, Rainy
        [0.2, 0.3, 0.5]   # Rainy -> Sunny, Cloudy, Rainy
    ])
    
    # Create Markov chain
    mc = MarkovChain(states=states, transition_matrix=transition_matrix)
    
    # Simulate weather for 10 days
    weather_path = mc.simulate(10, start_state="Sunny")
    print("Simulated weather path:", weather_path)
    
    # Compute stationary distribution
    stationary = mc.get_stationary_distribution()
    print("\nStationary distribution:")
    for state, prob in zip(states, stationary):
        print(f"  {state}: {prob:.3f}")
    
    # Compute hitting times to Rainy
    hitting_times = mc.get_hitting_time("Rainy")
    print("\nExpected hitting times to Rainy:")
    for state, time in hitting_times.items():
        print(f"  From {state}: {time:.2f} days")
    
    # Analyze communication classes
    classes = mc.analyze_communication_classes()
    print("\nCommunication classes:")
    for class_name, states_in_class in classes.items():
        print(f"  {class_name}: {states_in_class}")
    
    return mc

if __name__ == "__main__":
    example_markov_chain()
```

### Hidden Markov Model Implementation

```python
"""
Hidden Markov Model Implementation
"""

import numpy as np
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class HiddenMarkovModel:
    """Hidden Markov Model implementation"""
    
    states: List[str]              # Hidden states
    observations: List[str]        # Observable symbols
    transition_matrix: np.ndarray  # A: state transition probabilities
    emission_matrix: np.ndarray    # B: emission probabilities
    initial_distribution: np.ndarray # π: initial state probabilities
    
    def __post_init__(self):
        # Validate dimensions
        n_states = len(self.states)
        n_observations = len(self.observations)
        
        assert self.transition_matrix.shape == (n_states, n_states)
        assert self.emission_matrix.shape == (n_states, n_observations)
        assert len(self.initial_distribution) == n_states
        
        # Check probability constraints
        assert np.allclose(np.sum(self.transition_matrix, axis=1), 1.0)
        assert np.allclose(np.sum(self.emission_matrix, axis=1), 1.0)
        assert np.allclose(np.sum(self.initial_distribution), 1.0)
    
    def forward_algorithm(self, observations: List[str]) -> Tuple[np.ndarray, float]:
        """
        Forward algorithm for computing P(O|λ)
        
        Returns:
            alpha: Forward probabilities
            likelihood: P(O|λ)
        """
        T = len(observations)
        N = len(self.states)
        
        # Initialize alpha
        alpha = np.zeros((T, N))
        
        # Initial step
        obs_idx = self.observations.index(observations[0])
        alpha[0] = (self.initial_distribution * 
                   self.emission_matrix[:, obs_idx])
        
        # Forward step
        for t in range(1, T):
            obs_idx = self.observations.index(observations[t])
            alpha[t] = (alpha[t-1].dot(self.transition_matrix) * 
                       self.emission_matrix[:, obs_idx])
        
        # Compute likelihood
        likelihood = np.sum(alpha[T-1])
        
        return alpha, likelihood
    
    def backward_algorithm(self, observations: List[str]) -> np.ndarray:
        """
        Backward algorithm for computing β probabilities
        
        Returns:
            beta: Backward probabilities
        """
        T = len(observations)
        N = len(self.states)
        
        # Initialize beta
        beta = np.zeros((T, N))
        beta[T-1] = 1.0
        
        # Backward step
        for t in range(T-2, -1, -1):
            obs_idx = self.observations.index(observations[t+1])
            beta[t] = self.transition_matrix.dot(
                self.emission_matrix[:, obs_idx] * beta[t+1]
            )
        
        return beta
    
    def viterbi_algorithm(self, observations: List[str]) -> Tuple[List[str], float]:
        """
        Viterbi algorithm for finding most likely state sequence
        
        Returns:
            path: Most likely state sequence
            probability: Probability of the path
        """
        T = len(observations)
        N = len(self.states)
        
        # Initialize delta and psi
        delta = np.zeros((T, N))
        psi = np.zeros((T, N), dtype=int)
        
        # Initial step
        obs_idx = self.observations.index(observations[0])
        delta[0] = (self.initial_distribution * 
                   self.emission_matrix[:, obs_idx])
        
        # Recursion
        for t in range(1, T):
            obs_idx = self.observations.index(observations[t])
            for j in range(N):
                temp = delta[t-1] * self.transition_matrix[:, j]
                psi[t, j] = np.argmax(temp)
                delta[t, j] = np.max(temp) * self.emission_matrix[j, obs_idx]
        
        # Termination
        best_path_prob = np.max(delta[T-1])
        best_last_state = np.argmax(delta[T-1])
        
        # Path backtracking
        path = [0] * T
        path[T-1] = best_last_state
        
        for t in range(T-2, -1, -1):
            path[t] = psi[t+1, path[t+1]]
        
        # Convert to state names
        state_sequence = [self.states[state_idx] for state_idx in path]
        
        return state_sequence, best_path_prob
    
    def baum_welch_algorithm(self, observations: List[List[str]], 
                           max_iterations: int = 100, 
                           tolerance: float = 1e-6) -> None:
        """
        Baum-Welch algorithm for parameter estimation
        
        Args:
            observations: List of observation sequences
            max_iterations: Maximum number of iterations
            tolerance: Convergence tolerance
        """
        N = len(self.states)
        M = len(self.observations)
        
        for iteration in range(max_iterations):
            # Initialize accumulators
            xi_sum = np.zeros((N, N))
            gamma_sum = np.zeros(N)
            gamma_obs_sum = np.zeros((N, M))
            
            log_likelihood = 0.0
            
            # Expectation step
            for obs_seq in observations:
                # Forward and backward probabilities
                alpha, obs_likelihood = self.forward_algorithm(obs_seq)
                beta = self.backward_algorithm(obs_seq)
                
                log_likelihood += np.log(obs_likelihood)
                
                # Normalize alpha and beta
                alpha_norm = alpha / np.sum(alpha, axis=1, keepdims=True)
                beta_norm = beta / np.sum(beta, axis=1, keepdims=True)
                
                T = len(obs_seq)
                
                # Compute xi and gamma
                for t in range(T-1):
                    obs_idx_t1 = self.observations.index(obs_seq[t+1])
                    
                    # Compute xi[t, i, j]
                    for i in range(N):
                        for j in range(N):
                            xi_num = (alpha_norm[t, i] * 
                                     self.transition_matrix[i, j] * 
                                     self.emission_matrix[j, obs_idx_t1] * 
                                     beta_norm[t+1, j])
                            xi_sum[i, j] += xi_num
                    
                    # Compute gamma[t, i]
                    for i in range(N):
                        gamma_sum[i] += alpha_norm[t, i] * beta_norm[t, i]
                
                # Handle last time step for gamma
                for i in range(N):
                    gamma_sum[i] += alpha_norm[T-1, i] * beta_norm[T-1, i]
                
                # Compute gamma for observations
                for t in range(T):
                    obs_idx = self.observations.index(obs_seq[t])
                    for i in range(N):
                        gamma_obs_sum[i, obs_idx] += alpha_norm[t, i] * beta_norm[t, i]
            
            # Maximization step
            # Update transition matrix
            for i in range(N):
                for j in range(N):
                    self.transition_matrix[i, j] = xi_sum[i, j] / gamma_sum[i]
            
            # Update emission matrix
            for i in range(N):
                gamma_total = np.sum(gamma_obs_sum[i])
                for k in range(M):
                    self.emission_matrix[i, k] = gamma_obs_sum[i, k] / gamma_total
            
            # Update initial distribution
            self.initial_distribution = gamma_obs_sum[:, 0] / np.sum(gamma_obs_sum[:, 0])
            
            # Check convergence
            if iteration > 0 and abs(log_likelihood - prev_likelihood) < tolerance:
                print(f"Converged after {iteration+1} iterations")
                break
            
            prev_likelihood = log_likelihood
    
    def simulate_sequence(self, length: int) -> Tuple[List[str], List[str]]:
        """Simulate state and observation sequences"""
        # Choose initial state
        current_state = np.random.choice(len(self.states), p=self.initial_distribution)
        
        hidden_states = [self.states[current_state]]
        observations = []
        
        for _ in range(length - 1):
            # Sample next state
            next_state = np.random.choice(
                len(self.states), 
                p=self.transition_matrix[current_state]
            )
            
            # Sample observation
            obs_idx = np.random.choice(
                len(self.observations),
                p=self.emission_matrix[next_state]
            )
            
            hidden_states.append(self.states[next_state])
            observations.append(self.observations[obs_idx])
            current_state = next_state
        
        return hidden_states, observations

# Example usage with HMM
def example_hidden_markov_model():
    """Example: Part-of-Speech Tagging HMM"""
    
    # Define states (POS tags)
    states = ["Noun", "Verb", "Adjective"]
    
    # Define observations (words)
    observations = ["cat", "run", "big", "dog", "jump", "small"]
    
    # Define transition matrix (simplified)
    transition_matrix = np.array([
        [0.5, 0.3, 0.2],  # Noun -> Noun, Verb, Adjective
        [0.4, 0.4, 0.2],  # Verb -> Noun, Verb, Adjective
        [0.3, 0.3, 0.4]   # Adjective -> Noun, Verb, Adjective
    ])
    
    # Define emission matrix (simplified)
    emission_matrix = np.array([
        [0.6, 0.1, 0.1, 0.2, 0.0, 0.0],  # Noun emissions
        [0.0, 0.6, 0.0, 0.0, 0.3, 0.1],  # Verb emissions
        [0.1, 0.0, 0.6, 0.1, 0.0, 0.2]   # Adjective emissions
    ])
    
    # Define initial distribution
    initial_distribution = np.array([0.5, 0.3, 0.2])
    
    # Create HMM
    hmm = HiddenMarkovModel(
        states=states,
        observations=observations,
        transition_matrix=transition_matrix,
        emission_matrix=emission_matrix,
        initial_distribution=initial_distribution
    )
    
    # Simulate sequence
    hidden_states, observed_words = hmm.simulate_sequence(10)
    print("Simulated sequence:")
    print("Hidden states:", hidden_states)
    print("Observed words:", observed_words)
    
    # Viterbi decoding
    most_likely_states, path_prob = hmm.viterbi_algorithm(observed_words)
    print(f"\nViterbi decoding:")
    print("Most likely states:", most_likely_states)
    print(f"Path probability: {path_prob:.6f}")
    
    # Forward algorithm
    alpha, likelihood = hmm.forward_algorithm(observed_words)
    print(f"\nForward algorithm:")
    print(f"Sequence likelihood: {likelihood:.6f}")
    
    return hmm

if __name__ == "__main__":
    example_hidden_markov_model()
```

### Markov Decision Process with Value Iteration

```python
"""
Markov Decision Process with Value Iteration
"""

import numpy as np
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class MarkovDecisionProcess:
    """Markov Decision Process implementation"""
    
    states: List[str]
    actions: List[str]
    transition_probabilities: np.ndarray  # P[s, a, s']
    rewards: np.ndarray                   # R[s, a, s']
    discount_factor: float = 0.9
    
    def __post_init__(self):
        n_states = len(self.states)
        n_actions = len(self.actions)
        
        assert self.transition_probabilities.shape == (n_states, n_actions, n_states)
        assert self.rewards.shape == (n_states, n_actions, n_states)
        
        # Check transition probabilities sum to 1
        for s in range(n_states):
            for a in range(n_actions):
                assert np.allclose(np.sum(self.transition_probabilities[s, a]), 1.0)
    
    def value_iteration(self, max_iterations: int = 1000, 
                       tolerance: float = 1e-6) -> Tuple[np.ndarray, np.ndarray]:
        """
        Value iteration algorithm
        
        Returns:
            values: Value function
            policy: Optimal policy
        """
        n_states = len(self.states)
        n_actions = len(self.actions)
        
        # Initialize value function
        values = np.zeros(n_states)
        
        for iteration in range(max_iterations):
            # Store old values
            old_values = values.copy()
            
            # Update value function
            for s in range(n_states):
                # Compute Q-values for all actions
                q_values = np.zeros(n_actions)
                for a in range(n_actions):
                    # Expected reward for action a in state s
                    expected_reward = 0.0
                    for s_next in range(n_states):
                        expected_reward += (self.transition_probabilities[s, a, s_next] * 
                                          (self.rewards[s, a, s_next] + 
                                           self.discount_factor * old_values[s_next]))
                    q_values[a] = expected_reward
                
                # Choose best action
                values[s] = np.max(q_values)
            
            # Check convergence
            if np.max(np.abs(values - old_values)) < tolerance:
                print(f"Value iteration converged after {iteration+1} iterations")
                break
        
        # Extract policy
        policy = np.zeros(n_states, dtype=int)
        for s in range(n_states):
            q_values = np.zeros(n_actions)
            for a in range(n_actions):
                expected_reward = 0.0
                for s_next in range(n_states):
                    expected_reward += (self.transition_probabilities[s, a, s_next] * 
                                      (self.rewards[s, a, s_next] + 
                                       self.discount_factor * values[s_next]))
                q_values[a] = expected_reward
            policy[s] = np.argmax(q_values)
        
        return values, policy
    
    def policy_iteration(self, max_iterations: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Policy iteration algorithm
        
        Returns:
            values: Value function
            policy: Optimal policy
        """
        n_states = len(self.states)
        n_actions = len(self.actions)
        
        # Initialize policy randomly
        policy = np.random.randint(0, n_actions, n_states)
        
        for iteration in range(max_iterations):
            # Policy evaluation
            values = self._evaluate_policy(policy)
            
            # Policy improvement
            new_policy = self._improve_policy(values)
            
            # Check convergence
            if np.array_equal(policy, new_policy):
                print(f"Policy iteration converged after {iteration+1} iterations")
                break
            
            policy = new_policy
        
        return values, policy
    
    def _evaluate_policy(self, policy: np.ndarray) -> np.ndarray:
        """Evaluate a given policy"""
        n_states = len(self.states)
        
        # Set up system of linear equations: V = R_policy + γ * P_policy * V
        # Rearranged: (I - γ * P_policy) * V = R_policy
        
        P_policy = np.zeros((n_states, n_states))
        R_policy = np.zeros(n_states)
        
        for s in range(n_states):
            a = policy[s]
            P_policy[s] = self.transition_probabilities[s, a]
            R_policy[s] = np.sum(self.transition_probabilities[s, a] * self.rewards[s, a])
        
        # Solve linear system
        A = np.eye(n_states) - self.discount_factor * P_policy
        values = np.linalg.solve(A, R_policy)
        
        return values
    
    def _improve_policy(self, values: np.ndarray) -> np.ndarray:
        """Improve policy given value function"""
        n_states = len(self.states)
        n_actions = len(self.actions)
        
        new_policy = np.zeros(n_states, dtype=int)
        
        for s in range(n_states):
            # Compute Q-values for all actions
            q_values = np.zeros(n_actions)
            for a in range(n_actions):
                expected_value = 0.0
                for s_next in range(n_states):
                    expected_value += (self.transition_probabilities[s, a, s_next] * 
                                     (self.rewards[s, a, s_next] + 
                                      self.discount_factor * values[s_next]))
                q_values[a] = expected_value
            
            # Choose best action
            new_policy[s] = np.argmax(q_values)
        
        return new_policy
    
    def q_learning(self, episodes: int = 1000, learning_rate: float = 0.1, 
                   epsilon: float = 0.1, max_steps: int = 100) -> np.ndarray:
        """
        Q-learning algorithm (model-free)
        
        Returns:
            q_table: Q-values for all state-action pairs
        """
        n_states = len(self.states)
        n_actions = len(self.actions)
        
        # Initialize Q-table
        q_table = np.zeros((n_states, n_actions))
        
        for episode in range(episodes):
            # Start from random state
            state = np.random.randint(0, n_states)
            
            for step in range(max_steps):
                # Epsilon-greedy action selection
                if np.random.random() < epsilon:
                    action = np.random.randint(0, n_actions)
                else:
                    action = np.argmax(q_table[state])
                
                # Take action and observe next state and reward
                next_state_probs = self.transition_probabilities[state, action]
                next_state = np.random.choice(n_states, p=next_state_probs)
                
                reward = 0.0
                for s_next in range(n_states):
                    reward += next_state_probs[s_next] * self.rewards[state, action, s_next]
                
                # Q-learning update
                best_next_action = np.argmax(q_table[next_state])
                td_target = reward + self.discount_factor * q_table[next_state, best_next_action]
                td_error = td_target - q_table[state, action]
                q_table[state, action] += learning_rate * td_error
                
                state = next_state
        
        return q_table
    
    def simulate_policy(self, policy: np.ndarray, start_state: str, 
                       max_steps: int = 100) -> Tuple[List[str], List[str], float]:
        """
        Simulate policy execution
        
        Returns:
            states: State sequence
            actions: Action sequence
            total_reward: Total accumulated reward
        """
        current_state_idx = self.states.index(start_state)
        states = [start_state]
        actions = []
        total_reward = 0.0
        
        for _ in range(max_steps):
            # Choose action according to policy
            action_idx = policy[current_state_idx]
            action = self.actions[action_idx]
            actions.append(action)
            
            # Sample next state
            next_state_probs = self.transition_probabilities[current_state_idx, action_idx]
            next_state_idx = np.random.choice(len(self.states), p=next_state_probs)
            
            # Sample reward
            reward_probs = self.rewards[current_state_idx, action_idx]
            reward = np.random.choice(reward_probs, p=next_state_probs)
            
            total_reward += reward
            
            # Update state
            current_state_idx = next_state_idx
            states.append(self.states[current_state_idx])
        
        return states, actions, total_reward

# Example usage with MDP
def example_markov_decision_process():
    """Example: Grid World MDP"""
    
    # Define states (grid positions)
    states = ["(0,0)", "(0,1)", "(1,0)", "(1,1)"]
    
    # Define actions
    actions = ["Up", "Down", "Left", "Right"]
    
    # Define transition probabilities and rewards
    # Simple 2x2 grid with goal at (1,1)
    n_states = len(states)
    n_actions = len(actions)
    
    transition_probabilities = np.zeros((n_states, n_actions, n_states))
    rewards = np.zeros((n_states, n_actions, n_states))
    
    # Goal state (1,1) - absorbing
    goal_idx = 3
    for a in range(n_actions):
        transition_probabilities[goal_idx, a, goal_idx] = 1.0
        rewards[goal_idx, a, goal_idx] = 0.0
    
    # Other transitions (simplified - deterministic for this example)
    # (0,0): Right -> (0,1), Down -> (1,0)
    transition_probabilities[0, 3, 1] = 1.0  # Right
    transition_probabilities[0, 1, 2] = 1.0  # Down
    # Other actions stay in place
    for a in [0, 2]:  # Up, Left
        transition_probabilities[0, a, 0] = 1.0
    
    # (0,1): Left -> (0,0), Down -> (1,1)
    transition_probabilities[1, 2, 0] = 1.0  # Left
    transition_probabilities[1, 1, 3] = 1.0  # Down
    # Other actions stay in place
    for a in [0, 3]:  # Up, Right
        transition_probabilities[1, a, 1] = 1.0
    
    # (1,0): Up -> (0,0), Right -> (1,1)
    transition_probabilities[2, 0, 0] = 1.0  # Up
    transition_probabilities[2, 3, 3] = 1.0  # Right
    # Other actions stay in place
    for a in [1, 2]:  # Down, Left
        transition_probabilities[2, a, 2] = 1.0
    
    # Set rewards (goal has reward 10, others have small negative reward)
    for s in range(n_states):
        for a in range(n_actions):
            for s_next in range(n_states):
                if s_next == goal_idx:
                    rewards[s, a, s_next] = 10.0
                else:
                    rewards[s, a, s_next] = -0.1
    
    # Create MDP
    mdp = MarkovDecisionProcess(
        states=states,
        actions=actions,
        transition_probabilities=transition_probabilities,
        rewards=rewards,
        discount_factor=0.9
    )
    
    # Solve with value iteration
    values, policy = mdp.value_iteration()
    print("Value Iteration Results:")
    print("Values:", values)
    print("Policy:", [actions[a] for a in policy])
    
    # Solve with policy iteration
    values_pi, policy_pi = mdp.policy_iteration()
    print("\nPolicy Iteration Results:")
    print("Values:", values_pi)
    print("Policy:", [actions[a] for a in policy_pi])
    
    # Q-learning
    q_table = mdp.q_learning(episodes=1000)
    print("\nQ-learning Results:")
    print("Q-table shape:", q_table.shape)
    
    # Simulate optimal policy
    states_seq, actions_seq, total_reward = mdp.simulate_policy(policy, "(0,0)", 10)
    print(f"\nSimulation from (0,0):")
    print("States:", states_seq)
    print("Actions:", actions_seq)
    print(f"Total reward: {total_reward:.2f}")
    
    return mdp, policy

if __name__ == "__main__":
    example_markov_decision_process()
```

## Input Format

### Markov Model Configuration

```yaml
markov_model_config:
  model_type: "markov_chain|hidden_markov|markov_decision_process"
  
  markov_chain:
    states: array                # List of state names
    transition_matrix: array     # State transition probabilities
    initial_distribution: array  # Initial state probabilities
    analysis_options:
      stationary_distribution: boolean
      hitting_times: boolean
      communication_classes: boolean
      
  hidden_markov_model:
    hidden_states: array         # Hidden state names
    observations: array          # Observable symbol names
    transition_matrix: array     # State transition probabilities
    emission_matrix: array       # Emission probabilities
    initial_distribution: array  # Initial state probabilities
    training_options:
      algorithm: "baum_welch|viterbi"
      max_iterations: number
      convergence_tolerance: number
      
  markov_decision_process:
    states: array                # State names
    actions: array               # Action names
    transition_probabilities: array # P[s, a, s']
    rewards: array               # R[s, a, s']
    discount_factor: number      # Discount factor γ
    solution_method: "value_iteration|policy_iteration|q_learning"
    algorithm_parameters:
      max_iterations: number
      convergence_tolerance: number
      learning_rate: number      # For Q-learning
      epsilon: number            # For Q-learning
```

### Advanced Configuration

```yaml
advanced_markov_config:
  continuous_time:
    generator_matrix: array      # Q-matrix for CTMC
    time_horizon: number         # Simulation time horizon
    
  hierarchical_models:
    level_structure: array       # Hierarchy of model levels
    coupling_probabilities: array # Coupling between levels
    
  adaptive_models:
    adaptation_strategy: string  # How model adapts over time
    adaptation_rate: number      # Rate of adaptation
    memory_length: number        # How much history to remember
    
  multi_agent:
    agent_count: number          # Number of agents
    interaction_matrix: array    # Agent interaction probabilities
    coordination_strategy: string # How agents coordinate
```

## Output Format

### Markov Chain Analysis

```yaml
markov_chain_analysis:
  stationary_distribution: array # π vector
  convergence_properties:
    mixing_time: number          # Time to reach stationary distribution
    convergence_rate: number     # Rate of convergence
    ergodicity: boolean          # Whether chain is ergodic
    
  hitting_times: dict            # Expected hitting times to each state
  communication_classes:
    classes: array               # List of communication classes
    recurrence_properties: dict  # Transient/recurrent classification
    
  long_term_behavior:
    periodicity: number          # Period of the chain
    absorption_probabilities: dict # Probabilities of absorption
    limiting_distribution: array # Limiting distribution if exists
```

### Hidden Markov Model Results

```yaml
hmm_results:
  parameter_estimates:
    transition_matrix: array     # Estimated A matrix
    emission_matrix: array       # Estimated B matrix
    initial_distribution: array  # Estimated π vector
    
  sequence_analysis:
    most_likely_states: array    # Viterbi path
    state_posteriors: array      # Posterior state probabilities
    observation_likelihood: number # P(O|λ)
    
  training_metrics:
    log_likelihood_history: array # Log-likelihood over iterations
    convergence_iteration: number # Iteration when converged
    final_likelihood: number     # Final log-likelihood
    
  prediction_accuracy:
    state_prediction_accuracy: number # Accuracy of state prediction
    observation_prediction_accuracy: number # Accuracy of observation prediction
```

### MDP Solution

```yaml
mdp_solution:
  value_function: array          # V* vector
  optimal_policy: array          # π* vector
  q_values: array                # Q* matrix (if applicable)
  
  solution_metrics:
    iterations_to_convergence: number # Number of iterations
    convergence_tolerance: number # Tolerance achieved
    computation_time: number     # Time to solve
    
  policy_evaluation:
    expected_return: number      # Expected return under optimal policy
    policy_stability: boolean    # Whether policy converged
    value_stability: boolean     # Whether values converged
    
  simulation_results:
    average_reward: number       # Average reward over simulations
    policy_performance: number   # Performance metric
    exploration_metrics: dict    # Exploration statistics (for RL)
```

## Configuration Options

### Model Types

```yaml
model_types:
  discrete_markov_chain:
    description: "Discrete-time Markov chain with finite state space"
    best_for: ["simple_state_models", "transition_analysis", "stationary_analysis"]
    complexity: "O(n^2)"
    parameters: ["transition_matrix", "initial_distribution"]
    
  continuous_time_markov_chain:
    description: "Continuous-time Markov chain with exponential transitions"
    best_for: ["queueing_systems", "reliability_analysis", "population_dynamics"]
    complexity: "O(n^3)"
    parameters: ["generator_matrix", "time_horizon"]
    
  hidden_markov_model:
    description: "Markov model with hidden states and observable emissions"
    best_for: ["sequence_analysis", "speech_recognition", "bioinformatics"]
    complexity: "O(T*n^2)"
    parameters: ["hidden_states", "observations", "emission_matrix"]
    
  markov_decision_process:
    description: "Markov model with actions and rewards for decision making"
    best_for: ["reinforcement_learning", "optimal_control", "planning"]
    complexity: "O(iterations*n*m)"
    parameters: ["actions", "rewards", "discount_factor"]
```

### Solution Algorithms

```yaml
solution_algorithms:
  exact_methods:
    value_iteration:
      description: "Iterative method for finding optimal value function"
      best_for: ["small_to_medium_mdp", "guaranteed_convergence"]
      complexity: "O(iterations*n^2*m)"
      convergence: "Linear"
      
    policy_iteration:
      description: "Iterative method alternating between policy evaluation and improvement"
      best_for: ["medium_mdp", "faster_convergence"]
      complexity: "O(iterations*n^3)"
      convergence: "Quadratic"
      
  approximate_methods:
    q_learning:
      description: "Model-free reinforcement learning algorithm"
      best_for: ["large_mdp", "unknown_dynamics", "online_learning"]
      complexity: "O(episodes*steps)"
      convergence: "Asymptotic"
      
    monte_carlo_methods:
      description: "Simulation-based estimation of value functions"
      best_for: ["episodic_tasks", "model_free", "flexible_rewards"]
      complexity: "O(samples*episodes)"
      convergence: "Asymptotic"
```

## Error Handling

### Model Specification Errors

```yaml
model_specification_errors:
  invalid_transition_matrix:
    detection_strategy: "probability_sum_validation"
    recovery_strategy: "matrix_normalization"
    max_retries: 1
    fallback_action: "uniform_distribution"
  
  inconsistent_dimensions:
    detection_strategy: "dimension_consistency_check"
    recovery_strategy: "dimension_adjustment"
    max_retries: 1
    fallback_action: "error_report"
  
  non_ergodic_chain:
    detection_strategy: "communication_class_analysis"
    recovery_strategy: "add_small_transition_probabilities"
    max_retries: 2
    fallback_action: "warn_user"
```

### Algorithm Convergence Issues

```yaml
convergence_issues:
  slow_convergence:
    detection_strategy: "iteration_count_monitoring"
    recovery_strategy: "adaptive_learning_rate"
    max_retries: 2
    fallback_action: "alternative_algorithm"
  
  oscillation:
    detection_strategy: "value_function_oscillation_detection"
    recovery_strategy: "damping_factor_application"
    max_retries: 1
    fallback_action: "policy_iteration"
  
  numerical_instability:
    detection_strategy: "value_range_validation"
    recovery_strategy: "regularization"
    max_retries: 2
    fallback_action: "simplified_model"
```

## Performance Optimization

### Algorithm Optimization

```python
# Optimization: Sparse matrix operations for large state spaces
class SparseMarkovChain:
    """Markov chain with sparse matrix operations"""
    
    def __init__(self, states: List[str], transition_matrix: np.ndarray):
        from scipy.sparse import csr_matrix
        
        self.states = states
        self.transition_matrix = csr_matrix(transition_matrix)
        
    def get_stationary_distribution_sparse(self) -> np.ndarray:
        """Compute stationary distribution using sparse operations"""
        from scipy.sparse.linalg import eigs
        
        # Find eigenvector corresponding to eigenvalue 1
        eigenvalues, eigenvectors = eigs(
            self.transition_matrix.T, 
            k=1, 
            which='LM',
            sigma=1.0
        )
        
        stationary = np.real(eigenvectors[:, 0])
        return stationary / np.sum(stationary)
```

### Memory Optimization

```yaml
memory_optimization:
  sparse_representations:
    technique: "sparse_matrix_storage"
    memory_reduction: "70-95%"
    implementation: "compressed_sparse_row"
    
  incremental_computation:
    technique: "streaming_algorithms"
    memory_reduction: "unlimited_sequences"
    implementation: "online_learning"
    
  checkpointing:
    technique: "periodic_state_saving"
    memory_reduction: "bounded_memory_usage"
    implementation: "disk_based_storage"
    
  parallel_processing:
    technique: "distributed_computation"
    memory_reduction: "cluster_scaling"
    implementation: "mpi_implementation"
```

## Integration Examples

### With Time Series Analysis

```python
# Integration with time series for regime detection
class RegimeSwitchingModel:
    """Markov switching model for time series analysis"""
    
    def __init__(self, regimes: int, states: List[str]):
        self.regimes = regimes
        self.states = states
        self.hmm = None
        
    def fit_regime_model(self, time_series: np.ndarray):
        """Fit HMM to detect regime switches in time series"""
        # Discretize time series into observations
        observations = self._discretize_time_series(time_series)
        
        # Create HMM for regime detection
        self.hmm = HiddenMarkovModel(
            states=self.states,
            observations=list(set(observations)),
            transition_matrix=self._initialize_transition_matrix(),
            emission_matrix=self._initialize_emission_matrix(),
            initial_distribution=np.ones(self.regimes) / self.regimes
        )
        
        # Train HMM
        self.hmm.baum_welch_algorithm([observations])
        
        return self.hmm
    
    def detect_regimes(self, time_series: np.ndarray) -> List[str]:
        """Detect regimes in time series"""
        observations = self._discretize_time_series(time_series)
        regimes, _ = self.hmm.viterbi_algorithm(observations)
        return regimes
```

### With Reinforcement Learning

```python
# Integration with reinforcement learning for policy optimization
class MDPReinforcementLearner:
    """MDP-based reinforcement learning agent"""
    
    def __init__(self, mdp: MarkovDecisionProcess):
        self.mdp = mdp
        self.q_table = None
        self.exploration_rate = 1.0
        self.min_exploration_rate = 0.01
        self.exploration_decay = 0.995
    
    def learn_optimal_policy(self, episodes: int = 1000):
        """Learn optimal policy using Q-learning"""
        self.q_table = self.mdp.q_learning(
            episodes=episodes,
            learning_rate=0.1,
            epsilon=self.exploration_rate
        )
        
        # Decay exploration rate
        self.exploration_rate = max(
            self.min_exploration_rate, 
            self.exploration_rate * self.exploration_decay
        )
        
        return self.q_table
    
    def get_policy_from_q_table(self) -> np.ndarray:
        """Extract policy from Q-table"""
        return np.argmax(self.q_table, axis=1)
```

## Best Practices

1. **Model Selection**:
   - Choose appropriate model type based on problem characteristics
   - Validate model assumptions (Markov property, stationarity)
   - Use domain knowledge to constrain model structure

2. **Parameter Estimation**:
   - Use sufficient data for reliable parameter estimation
   - Apply regularization for sparse data
   - Validate parameter estimates with cross-validation

3. **Algorithm Selection**:
   - Use exact methods for small to medium problems
   - Apply approximate methods for large-scale problems
   - Consider computational constraints and accuracy requirements

4. **Model Validation**:
   - Test model predictions on held-out data
   - Validate assumptions through residual analysis
   - Check for overfitting through cross-validation

## Troubleshooting

### Common Issues

1. **Non-convergence**: Increase iterations, adjust learning rates, check for oscillations
2. **Poor predictions**: Check model assumptions, increase data, adjust model complexity
3. **High computational cost**: Use sparse representations, approximate methods, parallel processing
4. **Numerical instability**: Apply regularization, check for ill-conditioned matrices

### Debug Mode

```python
# Debug mode: Enhanced MDP debugging
class DebugMarkovModel:
    """Markov model with enhanced debugging capabilities"""
    
    def __init__(self, model_type: str):
        self.model_type = model_type
        self.debug_log = []
        self.convergence_analysis = {}
        self.sensitivity_analysis = {}
    
    def log_algorithm_step(self, step_data):
        """Log detailed algorithm information"""
        self.debug_log.append({
            'step': step_data['step'],
            'iteration': step_data['iteration'],
            'computation_time': step_data['computation_time'],
            'memory_usage': step_data['memory_usage'],
            'convergence_metric': step_data.get('convergence_metric', 0.0)
        })
    
    def analyze_convergence(self):
        """Analyze convergence patterns and issues"""
        self.convergence_analysis = {
            'convergence_rate': self._compute_convergence_rate(),
            'oscillation_detection': self._detect_oscillations(),
            'stability_metrics': self._compute_stability_metrics(),
            'bottlenecks': self._identify_bottlenecks()
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

### Markov Model Performance Metrics

```yaml
markov_model_metrics:
  convergence_metrics:
    convergence_rate: number     # Rate of convergence
    iterations_to_convergence: number # Number of iterations needed
    convergence_stability: number # Stability of convergence
    
  accuracy_metrics:
    prediction_accuracy: number  # Accuracy of predictions
    state_estimation_accuracy: number # Accuracy of state estimation
    parameter_estimation_accuracy: number # Accuracy of parameter estimates
    
  computational_metrics:
    computation_time: number     # Total computation time
    memory_usage: string         # Peak memory usage
    scalability: number          # Performance with increasing size
    
  model_quality_metrics:
    likelihood_score: number     # Model likelihood
    aic_score: number            # Akaike Information Criterion
    bic_score: number            # Bayesian Information Criterion
    cross_validation_score: number # Cross-validation performance
```

## Dependencies

- **Core Libraries**: NumPy, SciPy for mathematical operations
- **Optimization**: CVXPY, Pyomo for parameter optimization
- **Machine Learning**: scikit-learn for integration with ML methods
- **Reinforcement Learning**: Stable-Baselines3, RLlib for advanced RL
- **Time Series**: statsmodels, tslearn for time series integration
- **Visualization**: Matplotlib, Plotly for result visualization

## Version History

- **1.0.0**: Initial release with comprehensive Markov model frameworks
- **1.1.0**: Added continuous-time Markov chains and advanced HMM features
- **1.2.0**: Enhanced MDP algorithms with deep reinforcement learning integration
- **1.3.0**: Improved performance optimization and memory management
- **1.4.0**: Added hierarchical and adaptive Markov models
- **1.5.0**: Enhanced debugging tools and model validation techniques

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

To be provided dynamically during execution.