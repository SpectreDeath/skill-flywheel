import logging
import pickle
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import Mock

import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

logger = logging.getLogger(__name__)


class PredictivePreloader:
    """Predicts and preloads skills based on usage patterns."""
    
    def __init__(self, ml_manager: "MLModelManager", skill_manager: Any = None):
        self.ml_manager = ml_manager
        self.skill_manager = skill_manager
        self.usage_history: Dict[str, List[float]] = {}
        self.prediction_window = 300  # 5 minutes in seconds
        self.min_confidence = 0.6
    
    def record_usage(self, skill_name: str, timestamp: float | None = None):
        """Record skill usage for prediction."""
        ts = timestamp or time.time()
        if skill_name not in self.usage_history:
            self.usage_history[skill_name] = []
        self.usage_history[skill_name].append(ts)
        
        # Keep only last 100 entries
        if len(self.usage_history[skill_name]) > 100:
            self.usage_history[skill_name] = self.usage_history[skill_name][-100:]
    
    def extract_features(self, skill_name: str) -> np.ndarray:
        """Extract features for usage prediction."""
        history = self.usage_history.get(skill_name, [])
        
        if len(history) < 2:
            return np.array([0.0, 0.0, 0.0, 0.0, 0.0])
        
        now = time.time()
        recent = [ts for ts in history if now - ts < 3600]  # Last hour
        very_recent = [ts for ts in history if now - ts < 300]  # Last 5 min
        
        features = [
            len(history),  # Total usage count
            len(recent),   # Recent usage count
            len(very_recent),  # Very recent usage count
            (now - history[-1]) if history else 0,  # Time since last use
            np.std(np.diff(history)) if len(history) > 1 else 0,  # Usage interval std
        ]
        
        return np.array(features)
    
    def predict_next_usage(self, skill_name: str) -> float:
        """Predict probability of skill being used in next window."""
        features = self.extract_features(skill_name)
        return self.ml_manager.predict_skill_usage(skill_name, features)
    
    def get_skills_to_preload(self) -> List[str]:
        """Get list of skills that should be preloaded."""
        skills_to_preload = []
        
        for skill_name in self.usage_history:
            confidence = self.predict_next_usage(skill_name)
            if confidence >= self.min_confidence:
                skills_to_preload.append(skill_name)
        
        return skills_to_preload
    
    async def preload_skills(self):
        """Preload skills predicted to be used soon."""
        if not self.skill_manager:
            return
        
        skills = self.get_skills_to_preload()
        for skill_name in skills:
            try:
                await self.skill_manager.load_skill_dynamically(skill_name)
                logger.info(f"Preloaded skill: {skill_name}")
            except Exception as e:
                logger.warning(f"Failed to preload {skill_name}: {e}")


class AdaptiveCacheEviction:
    """Adaptive cache eviction based on predicted usage."""
    
    def __init__(self, ml_manager: "MLModelManager"):
        self.ml_manager = ml_manager
        self.access_patterns: Dict[str, List[float]] = {}
    
    def record_access(self, skill_name: str):
        """Record cache access."""
        if skill_name not in self.access_patterns:
            self.access_patterns[skill_name] = []
        self.access_patterns[skill_name].append(time.time())
        
        # Keep last 50 entries
        if len(self.access_patterns[skill_name]) > 50:
            self.access_patterns[skill_name] = self.access_patterns[skill_name][-50:]
    
    def calculate_eviction_score(self, skill_name: str) -> float:
        """Calculate eviction priority score (lower = more likely to evict)."""
        history = self.access_patterns.get(skill_name, [])
        
        if not history:
            return 0.0
        
        now = time.time()
        recency = 1.0 / (1.0 + (now - history[-1]) / 3600)  # Recency score
        frequency = len(history) / 50.0  # Frequency score
        
        # Predict future usage
        features = np.array([
            len(history),
            sum(1 for ts in history if now - ts < 3600),
            sum(1 for ts in history if now - ts < 300),
            (now - history[-1]) if history else 0,
            0.0,
        ])
        predicted_usage = self.ml_manager.predict_skill_usage(skill_name, features)
        
        return recency * 0.3 + frequency * 0.3 + predicted_usage * 0.4
    
    def get_skills_to_evict(self, cache_size: int, target_size: int) -> List[str]:
        """Get skills to evict when cache needs to shrink."""
        if cache_size <= target_size:
            return []
        
        scores = {
            name: self.calculate_eviction_score(name)
            for name in self.access_patterns
        }
        
        sorted_skills = sorted(scores.items(), key=lambda x: x[1])
        num_to_evict = cache_size - target_size
        
        return [name for name, _ in sorted_skills[:num_to_evict]]

class MLModelManager:
    """ML model manager for predictive analytics."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.models: Dict[str, Any] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        self.feature_encoders: Dict[str, LabelEncoder] = {}
        self.model_path = Path(config["ml"]["model_path"])
        self.model_path.mkdir(exist_ok=True, parents=True)
        
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize ML models with real sklearn implementations."""
        from sklearn.ensemble import RandomForestRegressor, IsolationForest
        from sklearn.linear_model import LinearRegression
        from sklearn.cluster import KMeans
        
        ml_config = self.config.get("ml") if isinstance(self.config, dict) else None
        if not ml_config:
            ml_config = {}
            
        algorithms = ml_config.get("algorithms") if isinstance(ml_config, dict) else None
        if not algorithms:
            algorithms = {
                "usage_prediction": "RandomForest",
                "anomaly_detection": "IsolationForest",
                "performance_optimization": "LinearRegression",
                "resource_optimization": "KMeans"
            }
        
        # Initialize real models
        if algorithms.get("usage_prediction") == "RandomForest":
            self.models["usage_prediction"] = RandomForestRegressor(n_estimators=100, random_state=42)
        
        if algorithms.get("anomaly_detection") == "IsolationForest":
            self.models["anomaly_detection"] = IsolationForest(contamination=0.1, random_state=42)
            
        if algorithms.get("performance_optimization") == "LinearRegression":
            self.models["performance_optimization"] = LinearRegression()
            
        if algorithms.get("resource_optimization") == "KMeans":
            self.models["resource_optimization"] = KMeans(n_clusters=3, random_state=42)
        
        # Load existing models if they exist
        for model_name in self.models:
            model_file = self.model_path / f"{model_name}_model.pkl"
            if model_file.exists():
                try:
                    with open(model_file, 'rb') as f:
                        self.models[model_name] = pickle.load(f)
                    logger.info(f"Loaded existing model for {model_name}")
                except Exception as e:
                    logger.warning(f"Failed to load existing model {model_name}: {e}")
    
    def train_usage_prediction_model(self, features: np.ndarray, targets: np.ndarray):
        """Train usage prediction model with error handling."""
        if "usage_prediction" not in self.models:
            return
        
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                features, targets, test_size=0.2, random_state=42
            )
            
            self.models["usage_prediction"].fit(X_train, y_train)
            predictions = self.models["usage_prediction"].predict(X_test)
            mse = mean_squared_error(y_test, predictions)
            
            model_file = self.model_path / "usage_prediction_model.pkl"
            with open(model_file, 'wb') as f:
                pickle.dump(self.models["usage_prediction"], f)
            
            logger.info(f"Usage prediction model trained with MSE: {mse}")
        except Exception as e:
            logger.error(f"Failed to train usage prediction model: {e}")
    
    def predict_skill_usage(self, skill_name: str, features: np.ndarray) -> float:
        """Predict skill usage probability."""
        if "usage_prediction" not in self.models:
            return 0.1
        
        try:
            prediction = self.models["usage_prediction"].predict(features.reshape(1, -1))
            return float(max(0.0, min(1.0, prediction[0])))
        except Exception as e:
            logger.debug(f"Prediction failed for {skill_name}: {e}")
            return 0.1
    
    def detect_anomalies(self, metrics: np.ndarray) -> bool:
        """Detect anomalies in system metrics."""
        if "anomaly_detection" not in self.models:
            return False
        
        try:
            anomaly_score = self.models["anomaly_detection"].decision_function(metrics.reshape(1, -1))
            return bool(anomaly_score[0] < -0.5)
        except Exception as e:
            logger.error(f"Anomaly detection failed: {e}")
            return False
