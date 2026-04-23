#!/usr/bin/env python3
"""
predictive-skill-loading

ML-based predictive skill preloading for Skill Flywheel
Uses historical usage patterns to predict and preload skills before they are needed.
"""

import logging
import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import numpy as np

logger = logging.getLogger(__name__)

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class SkillUsageTracker:
    """Track skill usage patterns over time."""
    
    def __init__(self):
        self.usage_history: Dict[str, List[float]] = defaultdict(list)
        
    def record_usage(self, skill_name: str, timestamp: Optional[float] = None):
        """Record skill usage timestamp."""
        ts = timestamp or time.time()
        self.usage_history[skill_name].append(ts)
        if len(self.usage_history[skill_name]) > 100:
            self.usage_history[skill_name] = self.usage_history[skill_name][-100:]
    
    def get_usage_frequency(self, skill_name: str, window_hours: float = 168.0) -> float:
        """Calculate usage frequency over time window (default 7 days)."""
        if skill_name not in self.usage_history:
            return 0.0
        window_seconds = window_hours * 3600
        now = time.time()
        recent = [ts for ts in self.usage_history[skill_name] if now - ts < window_seconds]
        return len(recent) / max(window_hours, 1)
    
    def get_cooccurrence_skills(self, skill_name: str, window_seconds: float = 300) -> Dict[str, float]:
        """Get skills that are frequently used together."""
        if skill_name not in self.usage_history:
            return {}
        cooccurrence = defaultdict(int)
        total = len(self.usage_history[skill_name])
        
        for ts in self.usage_history[skill_name]:
            for other_skill, times in self.usage_history.items():
                if other_skill == skill_name:
                    continue
                for other_ts in times:
                    if abs(ts - other_ts) < window_seconds:
                        cooccurrence[other_skill] += 1
        
        return {k: v / total for k, v in cooccurrence.items()}


class PredictiveSkillLoader:
    """ML-based predictive skill loading."""
    
    def __init__(self):
        self.tracker = SkillUsageTracker()
        self.model: Optional[RandomForestClassifier] = None
        self._build_model()
    
    def _build_model(self):
        """Build prediction model (placeholder)."""
        if SKLEARN_AVAILABLE:
            self.model = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
    
    def extract_features(self, skill_name: str) -> np.ndarray:
        """Extract feature vector for a skill."""
        freq_7d = self.tracker.get_usage_frequency(skill_name, window_hours=168)
        freq_1d = self.tracker.get_usage_frequency(skill_name, window_hours=24)
        cooc = self.tracker.get_cooccurrence_skills(skill_name)
        
        features = [
            freq_7d,
            freq_1d,
            freq_7d / max(freq_1d, 0.01),
            len(cooc),
            sum(cooc.values()),
        ]
        return np.array(features).reshape(1, -1)
    
    def predict_usage_probability(self, skill_name: str) -> float:
        """Predict probability of skill being used soon."""
        if not self.tracker.usage_history.get(skill_name):
            return 0.1
        if self.model is None:
            return min(1.0, self.tracker.get_usage_frequency(skill_name) / 10)
        try:
            features = self.extract_features(skill_name)
            prob = self.model.predict_proba(features)[0, 1] if hasattr(self.model, 'predict_proba') else 0.5
            return float(np.clip(prob, 0, 1))
        except Exception:
            return min(1.0, self.tracker.get_usage_frequency(skill_name) / 10)
    
    def get_preload_recommendations(self, top_k: int = 10) -> List[tuple]:
        """Get skills recommended for preloading."""
        scores = []
        for skill_name in self.tracker.usage_history.keys():
            prob = self.predict_usage_probability(skill_name)
            scores.append((skill_name, prob))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


def predictive_skill_loading(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Core implementation for predictive-skill-loading."""
    action = payload.get("action", "predict")
    
    # Get shared instance or create new
    loader = payload.get("_loader")
    if loader is None:
        loader = PredictiveSkillLoader()
    
    if action == "record":
        skill_name = payload.get("skill")
        if skill_name:
            loader.tracker.record_usage(skill_name)
            return {"status": "success", "skill": skill_name, "recorded": True}
        return {"status": "error", "message": "skill name required"}
    
    elif action == "predict":
        skill_name = payload.get("skill")
        if skill_name:
            prob = loader.predict_usage_probability(skill_name)
            return {"status": "success", "skill": skill_name, "probability": prob}
        recommendations = loader.get_preload_recommendations(top_k=payload.get("top_k", 10))
        return {"status": "success", "recommendations": recommendations}
    
    elif action == "process":
        return {"status": "success", "message": "predictive loading ready"}
    
    return {"status": "error", "message": f"Unknown action: {action}"}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "process")
    try:
        if action == "record":
            skill = payload.get("skill")
            if not skill:
                return {"result": {"error": "skill required"}, "metadata": {}}
            result = predictive_skill_loading({"action": "record", "skill": skill})
            return {"result": result, "metadata": {"action": action, "timestamp": datetime.now().isoformat()}}
        
        elif action == "predict":
            skill = payload.get("skill")
            if skill:
                result = predictive_skill_loading({"action": "predict", "skill": skill})
                return {"result": result, "metadata": {"action": action, "timestamp": datetime.now().isoformat()}}
            
            result = predictive_skill_loading({"action": "predict", "top_k": payload.get("top_k", 10)})
            return {"result": result, "metadata": {"action": action, "timestamp": datetime.now().isoformat()}}
        
        elif action == "process":
            result = {"action": "process", "status": "success", "message": "predictive loading ready"}
            return {"result": result, "metadata": {"action": action, "timestamp": datetime.now().isoformat()}}
        
        else:
            return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action}}}
    
    except Exception as e:
        logger.error(f"Error in predictive-skill-loading: {e}")
        return {"result": {"error": str(e)}, "metadata": {"action": action, "timestamp": datetime.now().isoformat()}}


def register_skill() -> Dict[str, str]:
    """Return skill metadata."""
    return {
        "name": "predictive-skill-loading",
        "description": "ML-based predictive skill preloading for Skill Flywheel",
        "version": "1.0.0",
        "domain": "ML_AI",
    }