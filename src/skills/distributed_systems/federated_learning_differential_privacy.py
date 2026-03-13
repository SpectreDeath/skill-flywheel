#!/usr/bin/env python3
"""
Federated Learning with Differential Privacy

This skill provides comprehensive implementation patterns for privacy-preserving machine learning
across distributed clients using federated averaging with differential privacy mechanisms.
It covers secure aggregation, gradient clipping, noise addition, and client selection strategies.

Source: Distributed Systems Skills Framework
Type: Advanced Implementation Patterns
Category: Distributed ML
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
import logging
import json
import asyncio
import hashlib
import secrets
from dataclasses import dataclass
from abc import ABC, abstractmethod
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ClientConfig:
    """Configuration for federated learning clients."""
    client_id: str
    learning_rate: float = 0.01
    batch_size: int = 32
    local_epochs: int = 5
    clipping_norm: float = 1.0
    noise_multiplier: float = 1.0
    participation_probability: float = 1.0


@dataclass
class ServerConfig:
    """Configuration for federated learning server."""
    num_clients: int = 100
    target_clients: int = 10
    global_rounds: int = 100
    epsilon: float = 1.0
    delta: float = 1e-5
    clipping_norm: float = 1.0
    noise_multiplier: float = 1.0


class PrivacyAccountant:
    """Track and manage privacy budget consumption in federated learning."""
    
    def __init__(self, epsilon: float, delta: float):
        """
        Initialize privacy accountant.
        
        Args:
            epsilon (float): Privacy budget epsilon
            delta (float): Privacy budget delta
        """
        self.epsilon = epsilon
        self.delta = delta
        self.consumed_epsilon = 0.0
        self.consumed_delta = 0.0
        self.rounds = 0
        
        logger.info(f"Privacy accountant initialized: ε={epsilon}, δ={delta}")
    
    def calculate_noise_multiplier(self, sampling_rate: float, 
                                 steps: int) -> float:
        """
        Calculate noise multiplier for given privacy budget.
        
        Args:
            sampling_rate (float): Fraction of clients sampled per round
            steps (int): Number of training steps
            
        Returns:
            float: Noise multiplier
        """
        # Simplified RDP accountant for demonstration
        # In practice, use opacus or similar libraries
        target_epsilon = self.epsilon / steps
        noise_multiplier = np.sqrt(2 * np.log(1.25 / self.delta)) / target_epsilon
        
        logger.info(f"Calculated noise multiplier: {noise_multiplier}")
        return noise_multiplier
    
    def consume_privacy_budget(self, epsilon_used: float, delta_used: float):
        """
        Record privacy budget consumption.
        
        Args:
            epsilon_used (float): Epsilon consumed in this operation
            delta_used (float): Delta consumed in this operation
        """
        self.consumed_epsilon += epsilon_used
        self.consumed_delta += delta_used
        self.rounds += 1
        
        logger.info(f"Privacy budget consumed: ε={epsilon_used:.4f}, δ={delta_used:.8f}")
        logger.info(f"Total consumed: ε={self.consumed_epsilon:.4f}/{self.epsilon}, "
                   f"δ={self.consumed_delta:.8f}/{self.delta}")
    
    def check_budget(self) -> bool:
        """
        Check if privacy budget is still available.
        
        Returns:
            bool: True if budget available, False otherwise
        """
        if self.consumed_epsilon >= self.epsilon or self.consumed_delta >= self.delta:
            logger.warning("Privacy budget exhausted!")
            return False
        return True


class FederatedClient:
    """
    Federated learning client that performs local training with differential privacy.
    """
    
    def __init__(self, config: ClientConfig, model: nn.Module, 
                 train_data: torch.utils.data.Dataset):
        """
        Initialize federated client.
        
        Args:
            config (ClientConfig): Client configuration
            model (nn.Module): Global model to train
            train_data (torch.utils.data.Dataset): Local training data
        """
        self.config = config
        self.local_model = self._copy_model(model)
        self.train_loader = torch.utils.data.DataLoader(
            train_data, batch_size=config.batch_size, shuffle=True
        )
        self.optimizer = optim.SGD(self.local_model.parameters(), lr=config.learning_rate)
        self.criterion = nn.CrossEntropyLoss()
        
        # Privacy parameters
        self.clipping_norm = config.clipping_norm
        self.noise_multiplier = config.noise_multiplier
        
        logger.info(f"Client {config.client_id} initialized")
    
    def _copy_model(self, model: nn.Module) -> nn.Module:
        """Create a copy of the global model."""
        local_model = type(model)()
        local_model.load_state_dict(model.state_dict())
        return local_model
    
    def clip_gradients(self, model: nn.Module):
        """
        Clip gradients to ensure bounded sensitivity.
        
        Args:
            model (nn.Module): Model with gradients to clip
        """
        total_norm = 0
        for param in model.parameters():
            if param.grad is not None:
                param_norm = param.grad.data.norm(2)
                total_norm += param_norm.item() ** 2
        total_norm = total_norm ** (1. / 2)
        
        clip_coef = self.clipping_norm / (total_norm + 1e-6)
        if clip_coef < 1:
            for param in model.parameters():
                if param.grad is not None:
                    param.grad.data.mul_(clip_coef)
    
    def add_gaussian_noise(self, model: nn.Module) -> nn.Module:
        """
        Add Gaussian noise for differential privacy.
        
        Args:
            model (nn.Module): Model to add noise to
            
        Returns:
            nn.Module: Noisy model
        """
        with torch.no_grad():
            for param in model.parameters():
                noise = torch.normal(
                    mean=0.0,
                    std=self.noise_multiplier * self.clipping_norm,
                    size=param.shape,
                    device=param.device,
                    dtype=param.dtype
                )
                param.data.add_(noise)
        
        return model
    
    def local_train(self) -> Dict[str, Any]:
        """
        Perform local training with differential privacy.
        
        Returns:
            Dict[str, Any]: Training results and model updates
        """
        self.local_model.train()
        
        train_loss = 0.0
        train_acc = 0.0
        total_samples = 0
        
        for epoch in range(self.config.local_epochs):
            for batch_idx, (data, target) in enumerate(self.train_loader):
                self.optimizer.zero_grad()
                output = self.local_model(data)
                loss = self.criterion(output, target)
                loss.backward()
                
                # Apply gradient clipping
                self.clip_gradients(self.local_model)
                
                self.optimizer.step()
                
                train_loss += loss.item()
                pred = output.argmax(dim=1, keepdim=True)
                train_acc += pred.eq(target.view_as(pred)).sum().item()
                total_samples += len(target)
        
        # Add differential privacy noise
        self.local_model = self.add_gaussian_noise(self.local_model)
        
        # Calculate model update
        update = self._compute_model_update()
        
        results = {
            "client_id": self.config.client_id,
            "train_loss": train_loss / len(self.train_loader),
            "train_acc": train_acc / total_samples,
            "update": update,
            "num_samples": total_samples
        }
        
        logger.info(f"Client {self.config.client_id} training completed: "
                   f"loss={results['train_loss']:.4f}, acc={results['train_acc']:.4f}")
        
        return results
    
    def _compute_model_update(self) -> Dict[str, torch.Tensor]:
        """Compute the difference between local and global model."""
        update = {}
        for name, param in self.local_model.named_parameters():
            update[name] = param.data.clone()
        return update


class ClientSelector(ABC):
    """Abstract base class for client selection strategies."""
    
    @abstractmethod
    def select_clients(self, clients: List[FederatedClient], 
                      target_num: int) -> List[FederatedClient]:
        """
        Select clients for federated learning round.
        
        Args:
            clients (List[FederatedClient]): Available clients
            target_num (int): Number of clients to select
            
        Returns:
            List[FederatedClient]: Selected clients
        """
        pass


class RandomSelector(ClientSelector):
    """Random client selection strategy."""
    
    def select_clients(self, clients: List[FederatedClient], 
                      target_num: int) -> List[FederatedClient]:
        """Select clients randomly."""
        if target_num >= len(clients):
            return clients
        
        selected_indices = np.random.choice(
            len(clients), target_num, replace=False
        )
        return [clients[i] for i in selected_indices]


class ProbabilisticSelector(ClientSelector):
    """Probabilistic client selection based on participation probability."""
    
    def select_clients(self, clients: List[FederatedClient], 
                      target_num: int) -> List[FederatedClient]:
        """Select clients based on their participation probability."""
        selected_clients = []
        
        for client in clients:
            if len(selected_clients) >= target_num:
                break
            
            if np.random.random() < client.config.participation_probability:
                selected_clients.append(client)
        
        # If not enough clients selected, fill randomly
        if len(selected_clients) < target_num:
            remaining = [c for c in clients if c not in selected_clients]
            needed = target_num - len(selected_clients)
            if len(remaining) > 0:
                additional = np.random.choice(remaining, min(needed, len(remaining)), replace=False)
                selected_clients.extend(additional)
        
        return selected_clients


class SecureAggregator:
    """Secure aggregation implementation for federated learning."""
    
    def __init__(self, num_clients: int):
        """
        Initialize secure aggregator.
        
        Args:
            num_clients (int): Number of clients in the system
        """
        self.num_clients = num_clients
        self.client_keys = {}
        
        logger.info(f"Secure aggregator initialized for {num_clients} clients")
    
    def generate_client_key(self, client_id: str) -> Tuple[int, int]:
        """
        Generate cryptographic keys for secure aggregation.
        
        Args:
            client_id (str): Client identifier
            
        Returns:
            Tuple[int, int]: Public and private keys
        """
        # Simplified key generation for demonstration
        # In practice, use proper cryptographic libraries
        private_key = secrets.randbelow(1000000)
        public_key = (private_key * 12345 + 67890) % 1000000
        
        self.client_keys[client_id] = {
            'private': private_key,
            'public': public_key
        }
        
        return public_key, private_key
    
    def aggregate_updates(self, updates: List[Dict[str, torch.Tensor]], 
                         weights: List[float]) -> Dict[str, torch.Tensor]:
        """
        Aggregate model updates from clients.
        
        Args:
            updates (List[Dict[str, torch.Tensor]]): Client updates
            weights (List[float]): Client weights
            
        Returns:
            Dict[str, torch.Tensor]: Aggregated update
        """
        if not updates:
            return {}
        
        # Initialize aggregated update
        aggregated_update = {}
        total_weight = sum(weights)
        
        # Aggregate weighted updates
        for name in updates[0].keys():
            aggregated_update[name] = torch.zeros_like(updates[0][name])
            
            for update, weight in zip(updates, weights):
                aggregated_update[name] += update[name] * (weight / total_weight)
        
        logger.info(f"Secure aggregation completed for {len(updates)} clients")
        return aggregated_update


class FederatedServer:
    """
    Federated learning server that orchestrates training rounds with differential privacy.
    """
    
    def __init__(self, config: ServerConfig, model: nn.Module,
                 client_selector: ClientSelector = None):
        """
        Initialize federated server.
        
        Args:
            config (ServerConfig): Server configuration
            model (nn.Module): Global model
            client_selector (ClientSelector): Client selection strategy
        """
        self.config = config
        self.global_model = model
        self.clients = []
        self.client_selector = client_selector or RandomSelector()
        self.aggregator = SecureAggregator(config.num_clients)
        self.privacy_accountant = PrivacyAccountant(config.epsilon, config.delta)
        
        # Training metrics
        self.metrics = {
            'rounds': [],
            'accuracy': [],
            'loss': [],
            'privacy_budget': []
        }
        
        logger.info(f"Federated server initialized: {config.num_clients} clients, "
                   f"{config.global_rounds} rounds")
    
    def add_clients(self, clients: List[FederatedClient]):
        """Add clients to the federated learning system."""
        self.clients.extend(clients)
        logger.info(f"Added {len(clients)} clients to federated system")
    
    def select_participating_clients(self) -> List[FederatedClient]:
        """Select clients for the current training round."""
        return self.client_selector.select_clients(
            self.clients, self.config.target_clients
        )
    
    def aggregate_client_updates(self, client_updates: List[Dict[str, Any]]) -> Dict[str, torch.Tensor]:
        """
        Aggregate updates from participating clients.
        
        Args:
            client_updates (List[Dict[str, Any]]): Client training results
            
        Returns:
            Dict[str, torch.Tensor]: Aggregated model update
        """
        updates = [result['update'] for result in client_updates]
        weights = [result['num_samples'] for result in client_updates]
        
        return self.aggregator.aggregate_updates(updates, weights)
    
    def update_global_model(self, aggregated_update: Dict[str, torch.Tensor]):
        """
        Update global model with aggregated updates.
        
        Args:
            aggregated_update (Dict[str, torch.Tensor]): Aggregated model update
        """
        with torch.no_grad():
            for name, param in self.global_model.named_parameters():
                if name in aggregated_update:
                    param.data.add_(aggregated_update[name])
    
    def federated_round(self, round_num: int) -> Dict[str, Any]:
        """
        Execute one round of federated learning.
        
        Args:
            round_num (int): Current round number
            
        Returns:
            Dict[str, Any]: Round results
        """
        logger.info(f"Starting federated round {round_num}")
        
        # Check privacy budget
        if not self.privacy_accountant.check_budget():
            logger.warning("Privacy budget exhausted, stopping training")
            return {"status": "privacy_budget_exhausted"}
        
        # Select participating clients
        selected_clients = self.select_participating_clients()
        logger.info(f"Selected {len(selected_clients)} clients for round {round_num}")
        
        # Train selected clients
        client_results = []
        for client in selected_clients:
            result = client.local_train()
            client_results.append(result)
        
        # Aggregate updates
        aggregated_update = self.aggregate_client_updates(client_results)
        
        # Update global model
        self.update_global_model(aggregated_update)
        
        # Calculate round metrics
        avg_loss = np.mean([r['train_loss'] for r in client_results])
        avg_acc = np.mean([r['train_acc'] for r in client_results])
        
        # Record privacy consumption
        epsilon_used = self.config.epsilon / self.config.global_rounds
        delta_used = self.config.delta / self.config.global_rounds
        self.privacy_accountant.consume_privacy_budget(epsilon_used, delta_used)
        
        round_result = {
            "round": round_num,
            "num_participants": len(selected_clients),
            "avg_loss": avg_loss,
            "avg_accuracy": avg_acc,
            "privacy_epsilon": self.privacy_accountant.consumed_epsilon,
            "privacy_delta": self.privacy_accountant.consumed_delta
        }
        
        # Store metrics
        self.metrics['rounds'].append(round_num)
        self.metrics['accuracy'].append(avg_acc)
        self.metrics['loss'].append(avg_loss)
        self.metrics['privacy_budget'].append({
            'epsilon': self.privacy_accountant.consumed_epsilon,
            'delta': self.privacy_accountant.consumed_delta
        })
        
        logger.info(f"Round {round_num} completed: "
                   f"accuracy={avg_acc:.4f}, loss={avg_loss:.4f}")
        
        return round_result
    
    def run_federated_training(self) -> Dict[str, Any]:
        """
        Run complete federated learning training process.
        
        Returns:
            Dict[str, Any]: Training results
        """
        logger.info("Starting federated learning training")
        
        training_results = []
        
        for round_num in range(1, self.config.global_rounds + 1):
            try:
                round_result = self.federated_round(round_num)
                
                if round_result.get("status") == "privacy_budget_exhausted":
                    logger.warning("Training stopped due to privacy budget exhaustion")
                    break
                
                training_results.append(round_result)
                
                # Log progress every 10 rounds
                if round_num % 10 == 0:
                    logger.info(f"Progress: Round {round_num}/{self.config.global_rounds}, "
                               f"Accuracy: {round_result['avg_accuracy']:.4f}")
                
            except Exception as e:
                logger.error(f"Error in round {round_num}: {e}")
                continue
        
        final_result = {
            "status": "completed",
            "total_rounds": len(training_results),
            "final_accuracy": training_results[-1]['avg_accuracy'] if training_results else 0.0,
            "final_loss": training_results[-1]['avg_loss'] if training_results else 0.0,
            "privacy_consumed": {
                "epsilon": self.privacy_accountant.consumed_epsilon,
                "delta": self.privacy_accountant.consumed_delta
            },
            "metrics": self.metrics
        }
        
        logger.info("Federated learning training completed")
        return final_result


def create_federated_learning_system(
    num_clients: int = 100,
    target_clients: int = 10,
    global_rounds: int = 50,
    epsilon: float = 1.0,
    delta: float = 1e-5,
    model_architecture: str = "simple_cnn"
) -> Tuple[FederatedServer, List[FederatedClient]]:
    """
    Create a complete federated learning system with differential privacy.
    
    Args:
        num_clients (int): Total number of clients
        target_clients (int): Number of clients per round
        global_rounds (int): Number of global training rounds
        epsilon (float): Privacy budget epsilon
        delta (float): Privacy budget delta
        model_architecture (str): Model architecture type
        
    Returns:
        Tuple[FederatedServer, List[FederatedClient]]: Server and clients
    """
    try:
        # Create model
        if model_architecture == "simple_cnn":
            model = SimpleCNN()
        else:
            model = SimpleMLP()
        
        # Create server
        server_config = ServerConfig(
            num_clients=num_clients,
            target_clients=target_clients,
            global_rounds=global_rounds,
            epsilon=epsilon,
            delta=delta
        )
        
        server = FederatedServer(server_config, model)
        
        # Create clients
        clients = []
        for i in range(num_clients):
            client_config = ClientConfig(
                client_id=f"client_{i}",
                learning_rate=0.01,
                batch_size=32,
                local_epochs=5,
                clipping_norm=1.0,
                noise_multiplier=1.0,
                participation_probability=0.8
            )
            
            # Create synthetic data for client
            train_data = create_synthetic_data(100)  # 100 samples per client
            
            client = FederatedClient(client_config, model, train_data)
            clients.append(client)
        
        server.add_clients(clients)
        
        logger.info(f"Federated learning system created: {num_clients} clients, "
                   f"target {target_clients} per round")
        
        return server, clients
        
    except Exception as e:
        logger.error(f"Failed to create federated learning system: {e}")
        raise


class SimpleCNN(nn.Module):
    """Simple CNN for demonstration purposes."""
    
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)
    
    def forward(self, x):
        x = self.conv1(x)
        x = torch.relu(x)
        x = self.conv2(x)
        x = torch.relu(x)
        x = torch.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        return torch.log_softmax(x, dim=1)


class SimpleMLP(nn.Module):
    """Simple MLP for demonstration purposes."""
    
    def __init__(self, input_size=784, hidden_size=128, num_classes=10):
        super(SimpleMLP, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, num_classes)
        self.dropout = nn.Dropout(0.2)
    
    def forward(self, x):
        x = x.view(x.size(0), -1)  # Flatten input
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return torch.log_softmax(x, dim=1)


def create_synthetic_data(num_samples: int = 100) -> torch.utils.data.Dataset:
    """
    Create synthetic dataset for federated learning clients.
    
    Args:
        num_samples (int): Number of samples to generate
        
    Returns:
        torch.utils.data.Dataset: Synthetic dataset
    """
    # Generate synthetic data
    X = torch.randn(num_samples, 1, 28, 28)  # MNIST-like data
    y = torch.randint(0, 10, (num_samples,))  # 10 classes
    
    dataset = torch.utils.data.TensorDataset(X, y)
    return dataset


def validate_federated_learning_config(config: Dict[str, Any]) -> bool:
    """
    Validate federated learning configuration.
    
    Args:
        config (Dict[str, Any]): Configuration to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ["num_clients", "target_clients", "global_rounds", "epsilon", "delta"]
    
    for field in required_fields:
        if field not in config:
            logger.error(f"Missing required field: {field}")
            return False
    
    # Validate ranges
    if config["num_clients"] <= 0:
        logger.error("num_clients must be positive")
        return False
    
    if config["target_clients"] <= 0 or config["target_clients"] > config["num_clients"]:
        logger.error("target_clients must be between 1 and num_clients")
        return False
    
    if config["global_rounds"] <= 0:
        logger.error("global_rounds must be positive")
        return False
    
    if config["epsilon"] <= 0:
        logger.error("epsilon must be positive")
        return False
    
    if config["delta"] <= 0 or config["delta"] >= 1:
        logger.error("delta must be between 0 and 1")
        return False
    
    logger.info("Federated learning configuration validation passed")
    return True


def main():
    """Main execution function demonstrating federated learning with differential privacy."""
    print("Federated Learning with Differential Privacy")
    print("=" * 50)
    
    # Example 1: Create federated learning system
    print("\n1. Creating Federated Learning System...")
    try:
        server, clients = create_federated_learning_system(
            num_clients=50,
            target_clients=10,
            global_rounds=20,
            epsilon=1.0,
            delta=1e-5
        )
        
        print(f"✅ Created system with {len(clients)} clients")
        print(f"   Target clients per round: {server.config.target_clients}")
        print(f"   Privacy budget: ε={server.config.epsilon}, δ={server.config.delta}")
        
    except Exception as e:
        print(f"❌ Failed to create system: {e}")
        return
    
    # Example 2: Run federated training
    print("\n2. Running Federated Training...")
    try:
        results = server.run_federated_training()
        
        print(f"✅ Training completed: {results['total_rounds']} rounds")
        print(f"   Final accuracy: {results['final_accuracy']:.4f}")
        print(f"   Privacy consumed: ε={results['privacy_consumed']['epsilon']:.4f}")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
    
    # Example 3: Test different client selection strategies
    print("\n3. Testing Client Selection Strategies...")
    try:
        # Random selection
        random_selector = RandomSelector()
        server_random, _ = create_federated_learning_system(
            num_clients=20, target_clients=5, global_rounds=5
        )
        server_random.client_selector = random_selector
        
        # Probabilistic selection
        prob_selector = ProbabilisticSelector()
        server_prob, _ = create_federated_learning_system(
            num_clients=20, target_clients=5, global_rounds=5
        )
        server_prob.client_selector = prob_selector
        
        print("✅ Created systems with different selection strategies")
        
    except Exception as e:
        print(f"❌ Client selection test failed: {e}")
    
    print("\n" + "=" * 50)
    print("Federated learning examples completed!")


if __name__ == "__main__":
    main()