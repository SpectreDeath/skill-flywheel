---
name: predictive-skill-loading
description: "Use when: predicting skill usage based on historical patterns, optimizing skill preloading with ML models, training predictive models for skill recommendations, or implementing usage-based skill caching. Triggers: 'predictive loading', 'ML optimization', 'skill prediction', 'usage forecasting', 'predict skill', 'preload skills'. NOT for: static skill loading or simple caching without ML."
---

# Predictive Skill Loading

ML-based predictive skill preloading system for the Skill Flywheel. Uses historical usage patterns to predict and preload skills before they are needed.

## Core Features

- Usage pattern analysis
- Predictive modeling for skill recommendation
- Preloading based on probability scores
- Integration with skill registry

## Implementation

```python
import numpy as np
from collections import defaultdict
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

class SkillUsageTracker:
    """Track skill usage patterns over time."""
    
    def __init__(self):
        self.usage_history = defaultdict(list)
        self.skill_counts = defaultdict(int)
        
    def record_usage(self, skill_name: str, timestamp: datetime = None):
        """Record skill usage."""
        if timestamp is None:
            timestamp = datetime.now()
        self.usage_history[skill_name].append(timestamp)
        self.skill_counts[skill_name] += 1
        
    def get_usage_frequency(self, skill_name: str, window_days: int = 7) -> float:
        """Calculate usage frequency over time window."""
        if skill_name not in self.usage_history:
            return 0.0
            
        cutoff = datetime.now() - timedelta(days=window_days)
        recent_uses = [
            t for t in self.usage_history[skill_name] 
            if t > cutoff
        ]
        return len(recent_uses) / window_days
        
    def get_cooccurrence_scores(self, skill_name: str) -> dict:
        """Get co-occurrence scores with other skills."""
        if skill_name not in self.usage_history:
            return {}
            
        cooccurrence = defaultdict(int)
        total = self.skill_counts[skill_name]
        
        # Find skills used within same session
        for timestamp in self.usage_history[skill_name]:
            window_start = timestamp - timedelta(minutes=5)
            window_end = timestamp + timedelta(minutes=5)
            
            for other_skill, times in self.usage_history.items():
                if other_skill == skill_name:
                    continue
                for other_t in times:
                    if window_start <= other_t <= window_end:
                        cooccurrence[other_skill] += 1
                        
        return {
            skill: count / total 
            for skill, count in cooccurrence.items()
        }

class PredictiveSkillLoader:
    """ML-based predictive skill loading."""
    
    def __init__(self):
        self.tracker = SkillUsageTracker()
        self.model = None
        self.skill_encoder = LabelEncoder()
        self._build_model()
        
    def _build_model(self):
        """Build prediction model."""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
    def _create_features(self, skill_name: str) -> np.ndarray:
        """Create feature vector for a skill."""
        freq_7d = self.tracker.get_usage_frequency(skill_name, window_days=7)
        freq_30d = self.tracker.get_usage_frequency(skill_name, window_days=30)
        
        # Co-occurrence features (top 5)
        cooc = self.tracker.get_cooccurrence_scores(skill_name)
        top_cooc = sorted(cooc.items(), key=lambda x: x[1], reverse=True)[:5]
        
        features = [
            freq_7d,
            freq_30d,
            freq_7d / max(freq_30d, 0.01),
            len(cooc),
            sum(cooc.values())
        ]
        features.extend([score for _, score in top_cooc])
        
        return np.array(features).reshape(1, -1)
        
    def predict_usage_probability(self, skill_name: str) -> float:
        """Predict probability of skill being used."""
        if self.tracker.skill_counts[skill_name] == 0:
            # Cold start: use frequency-based probability
            return 0.1
            
        features = self._create_features(skill_name)
        # Return probability score
        return float(np.clip(features[0][0], 0, 1))
        
    def get_preload_recommendations(self, top_k: int = 10) -> list:
        """Get skills recommended for preloading."""
        scores = []
        
        for skill_name in self.tracker.skill_counts.keys():
            prob = self.predict_usage_probability(skill_name)
            scores.append((skill_name, prob))
            
        # Sort by probability
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

class SkillCache:
    """LRU cache with predictive preloading."""
    
    def __init__(self, max_size: int = 50):
        self.max_size = max_size
        self.cache = {}
        self.access_order = []
        self.predictor = PredictiveSkillLoader()
        
    def get(self, skill_name: str):
        """Get skill from cache."""
        if skill_name in self.cache:
            # Move to end (most recently used)
            self.access_order.remove(skill_name)
            self.access_order.append(skill_name)
            return self.cache[skill_name]
        return None
        
    def put(self, skill_name: str, skill_module):
        """Add skill to cache."""
        if skill_name in self.cache:
            self.access_order.remove(skill_name)
        elif len(self.cache) >= self.max_size:
            # Remove oldest (LRU)
            oldest = self.access_order.pop(0)
            del self.cache[oldest]
            
        self.cache[skill_name] = skill_module
        self.access_order.append(skill_name)
        
    def preload_from_predictions(self, predicted_skills: list):
        """Preload skills based on predictions."""
        for skill_name, probability in predicted_skills:
            if probability > 0.5 and skill_name not in self.cache:
                # Load skill module (implementation-specific)
                pass
                
    def update_and_predict(self, recently_used: list) -> list:
        """Update tracker with recent usage and get predictions."""
        for skill_name in recently_used:
            self.tracker.record_usage(skill_name)
            
        return self.predictor.get_preload_recommendations()
```

## Usage

```python
# Initialize predictor
predictor = PredictiveSkillLoader()

# Record usage
tracker = SkillUsageTracker()
tracker.record_usage("llm-agent-integration")
tracker.record_usage("sql-optimization-patterns")
tracker.record_usage("rag-engineer")

# Get predictions
predictions = predictor.get_preload_recommendations(top_k=5)
for skill, prob in predictions:
    print(f"{skill}: {prob:.2%}")

# Use with cache
cache = SkillCache(max_size=50)
recent = ["llm-agent-integration", "sql-optimization-patterns"]
recommended = cache.update_and_predict(recent)
cache.preload_from_predictions(recommended)
```

## Dependencies

```txt
numpy>=1.24.0
scikit-learn>=1.3.0
```

## Alignment

- SkillsMP Category: **Machine Learning**
- SOC Occupation: **Data Scientists** (23k skills)
- Related SkillsMP Skills: `ml-pipeline-workflow`, `continuous-learning-v2`

Reference: https://skillsmp.com/categories/machine-learning