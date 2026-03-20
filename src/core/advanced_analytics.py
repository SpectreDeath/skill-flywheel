#!/usr/bin/env python3
"""
Advanced Analytics and Machine Learning Integration for Skill Flywheel

This module provides advanced analytics capabilities including predictive performance
optimization, intelligent skill recommendations, automated quality improvement,
and anomaly detection for the enhanced MCP server.
"""

import asyncio
import logging
import statistics
import warnings
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

# ML and Analytics imports
try:
    import joblib
    from sklearn.cluster import KMeans
    from sklearn.ensemble import IsolationForest, RandomForestRegressor
    from sklearn.metrics import accuracy_score, mean_squared_error
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    warnings.warn("ML libraries not available. Some features will be disabled.", stacklevel=2)

logger = logging.getLogger(__name__)

class AnomalyType(Enum):
    PERFORMANCE = "performance"
    QUALITY = "quality"
    USAGE = "usage"
    SECURITY = "security"

class RecommendationType(Enum):
    OPTIMIZATION = "optimization"
    QUALITY_IMPROVEMENT = "quality_improvement"
    RESOURCE_ALLOCATION = "resource_allocation"
    SKILL_SELECTION = "skill_selection"

@dataclass
class AnomalyDetection:
    """Anomaly detection result."""
    anomaly_id: str
    anomaly_type: AnomalyType
    skill_id: str
    timestamp: datetime
    severity: str  # low, medium, high, critical
    description: str
    metrics: Dict[str, Any]
    suggested_actions: List[str]

@dataclass
class SkillRecommendation:
    """Intelligent skill recommendation."""
    recommendation_id: str
    recommendation_type: RecommendationType
    skill_id: str
    confidence_score: float
    description: str
    actions: List[str]
    expected_impact: Dict[str, Any]
    timestamp: datetime

@dataclass
class PredictiveInsight:
    """Predictive performance insight."""
    insight_id: str
    skill_id: str
    prediction_type: str
    predicted_value: float
    confidence_interval: Tuple[float, float]
    time_horizon: str
    factors: List[str]
    timestamp: datetime

class PerformancePredictor:
    """ML-based performance prediction system."""
    
    def __init__(self, model_path: Path):
        self.model_path = model_path
        self.model_path.mkdir(parents=True, exist_ok=True)
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        
        # Performance metrics history
        self.performance_history = defaultdict(deque)
        self.max_history_length = 1000
        
    def collect_training_data(self, skill_id: str, metrics: Dict[str, float]) -> bool:
        """Collect training data for ML models."""
        if not ML_AVAILABLE:
            return False
            
        try:
            # Add to history
            self.performance_history[skill_id].append({
                "timestamp": datetime.now().isoformat(),
                **metrics
            })
            
            # Maintain history size
            if len(self.performance_history[skill_id]) > self.max_history_length:
                self.performance_history[skill_id].popleft()
            
            return True
            
        except Exception as e:
            logger.error(f"Error collecting training data for {skill_id}: {e}")
            return False
    
    def train_performance_model(self, skill_id: str) -> bool:
        """Train ML model for performance prediction."""
        if not ML_AVAILABLE:
            return False
            
        try:
            history = list(self.performance_history[skill_id])
            if len(history) < 50:  # Minimum data points for training
                logger.warning(f"Insufficient data for training {skill_id}: {len(history)} points")
                return False
            
            # Prepare features
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Feature engineering
            features = self._extract_features(df)
            target = df['execution_time'].values
            
            if len(features) < len(target):
                logger.warning(f"Feature extraction failed for {skill_id}")
                return False
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                features, target, test_size=0.2, random_state=42
            )
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            
            logger.info(f"Model trained for {skill_id}: RMSE = {rmse:.4f}")
            
            # Save model and scaler
            model_file = self.model_path / f"{skill_id}_model.pkl"
            scaler_file = self.model_path / f"{skill_id}_scaler.pkl"
            
            joblib.dump(model, model_file)
            joblib.dump(scaler, scaler_file)
            
            # Store feature importance
            self.feature_importance[skill_id] = dict(zip(
                self._get_feature_names(), model.feature_importances_, strict=False
            ))
            
            return True
            
        except Exception as e:
            logger.error(f"Error training model for {skill_id}: {e}")
            return False
    
    def _extract_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract features for ML model."""
        
        # Time-based features
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # Rolling statistics
        for window in [5, 10, 20]:
            df[f'rolling_mean_{window}'] = df['execution_time'].rolling(window=window).mean()
            df[f'rolling_std_{window}'] = df['execution_time'].rolling(window=window).std()
            df[f'rolling_min_{window}'] = df['execution_time'].rolling(window=window).min()
            df[f'rolling_max_{window}'] = df['execution_time'].rolling(window=window).max()
        
        # Lag features
        for lag in [1, 2, 3]:
            df[f'lag_{lag}'] = df['execution_time'].shift(lag)
        
        # Fill NaN values
        df = df.fillna(df.mean())
        
        # Select feature columns
        feature_cols = [col for col in df.columns if col not in ['timestamp', 'execution_time']]
        
        return df[feature_cols].values
    
    def _get_feature_names(self) -> List[str]:
        """Get feature names for the model."""
        return [
            'hour', 'day_of_week', 'is_weekend',
            'rolling_mean_5', 'rolling_std_5', 'rolling_min_5', 'rolling_max_5',
            'rolling_mean_10', 'rolling_std_10', 'rolling_min_10', 'rolling_max_10',
            'rolling_mean_20', 'rolling_std_20', 'rolling_min_20', 'rolling_max_20',
            'lag_1', 'lag_2', 'lag_3'
        ]
    
    def predict_performance(self, skill_id: str, horizon_hours: int = 24) -> PredictiveInsight | None:
        """Predict future performance metrics."""
        if not ML_AVAILABLE:
            return None
            
        try:
            # Load model and scaler
            model_file = self.model_path / f"{skill_id}_model.pkl"
            scaler_file = self.model_path / f"{skill_id}_scaler.pkl"
            
            if not model_file.exists() or not scaler_file.exists():
                logger.warning(f"No trained model found for {skill_id}")
                return None
            
            model = joblib.load(model_file)
            scaler = joblib.load(scaler_file)
            
            # Create future features
            current_time = datetime.now()
            future_features = []
            
            for hour_ahead in range(horizon_hours):
                future_time = current_time + timedelta(hours=hour_ahead)
                
                # Create feature vector for future time
                features = self._create_future_features(skill_id, future_time)
                future_features.append(features)
            
            future_features = np.array(future_features)
            future_features_scaled = scaler.transform(future_features)
            
            # Predict
            predictions = model.predict(future_features_scaled)
            
            # Calculate confidence intervals (simplified)
            mean_pred = np.mean(predictions)
            std_pred = np.std(predictions)
            confidence_interval = (mean_pred - 1.96 * std_pred, mean_pred + 1.96 * std_pred)
            
            # Get important factors
            important_factors = sorted(
                self.feature_importance[skill_id].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            return PredictiveInsight(
                insight_id=f"prediction_{skill_id}_{datetime.now().isoformat()}",
                skill_id=skill_id,
                prediction_type="execution_time",
                predicted_value=mean_pred,
                confidence_interval=confidence_interval,
                time_horizon=f"{horizon_hours}h",
                factors=[factor[0] for factor in important_factors],
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error predicting performance for {skill_id}: {e}")
            return None
    
    def _create_future_features(self, skill_id: str, future_time: datetime) -> List[float]:
        """Create feature vector for a future time point."""
        features = []
        
        # Time features
        features.append(future_time.hour)
        features.append(future_time.weekday())
        features.append(1 if future_time.weekday() >= 5 else 0)
        
        # Rolling statistics (use recent averages)
        recent_history = list(self.performance_history[skill_id])[-10:]
        if recent_history:
            recent_times = [h['execution_time'] for h in recent_history]
            recent_mean = statistics.mean(recent_times)
            recent_std = statistics.stdev(recent_times) if len(recent_times) > 1 else 0
            recent_min = min(recent_times)
            recent_max = max(recent_times)
        else:
            recent_mean = recent_std = recent_min = recent_max = 0
        
        # Rolling statistics for different windows
        for _window in [5, 10, 20]:
            features.extend([recent_mean, recent_std, recent_min, recent_max])
        
        # Lag features (use recent values)
        recent_values = [h['execution_time'] for h in recent_history[-3:]]
        while len(recent_values) < 3:
            recent_values.append(recent_mean)
        
        features.extend(recent_values)
        
        return features

class AnomalyDetector:
    """Advanced anomaly detection system."""
    
    def __init__(self, sensitivity: float = 0.1):
        self.sensitivity = sensitivity
        self.detectors = {}
        self.baseline_metrics = defaultdict(dict)
        self.anomalies = []
        
    def update_baseline(self, skill_id: str, metrics: Dict[str, float]):
        """Update baseline metrics for anomaly detection."""
        if skill_id not in self.baseline_metrics:
            self.baseline_metrics[skill_id] = {
                "execution_time": [],
                "success_rate": [],
                "quality_score": [],
                "resource_usage": []
            }
        
        # Update rolling baseline
        for metric_name, value in metrics.items():
            if metric_name in self.baseline_metrics[skill_id]:
                baseline = self.baseline_metrics[skill_id][metric_name]
                baseline.append(value)
                
                # Keep only last 100 values
                if len(baseline) > 100:
                    baseline.pop(0)
    
    def detect_anomalies(self, skill_id: str, current_metrics: Dict[str, float]) -> List[AnomalyDetection]:
        """Detect anomalies in current metrics."""
        anomalies = []
        
        baseline = self.baseline_metrics.get(skill_id, {})
        if not baseline:
            return anomalies
        
        for metric_name, current_value in current_metrics.items():
            if metric_name not in baseline:
                continue
            
            baseline_values = baseline[metric_name]
            if len(baseline_values) < 20:  # Need sufficient baseline
                continue
            
            # Calculate statistics
            mean_val = statistics.mean(baseline_values)
            std_val = statistics.stdev(baseline_values) if len(baseline_values) > 1 else 0
            
            if std_val == 0:
                continue
            
            # Z-score based detection
            z_score = abs((current_value - mean_val) / std_val)
            
            if z_score > 3:  # 3-sigma rule
                severity = "critical" if z_score > 4 else "high" if z_score > 3.5 else "medium"
                
                anomaly = AnomalyDetection(
                    anomaly_id=f"anomaly_{skill_id}_{metric_name}_{datetime.now().isoformat()}",
                    anomaly_type=self._get_anomaly_type(metric_name),
                    skill_id=skill_id,
                    timestamp=datetime.now(),
                    severity=severity,
                    description=f"{metric_name} anomaly detected: {current_value:.4f} (expected: {mean_val:.4f} ± {std_val:.4f})",
                    metrics={
                        "current_value": current_value,
                        "baseline_mean": mean_val,
                        "baseline_std": std_val,
                        "z_score": z_score
                    },
                    suggested_actions=self._get_suggested_actions(metric_name, z_score)
                )
                
                anomalies.append(anomaly)
        
        # Store detected anomalies
        self.anomalies.extend(anomalies)
        
        return anomalies
    
    def _get_anomaly_type(self, metric_name: str) -> AnomalyType:
        """Determine anomaly type based on metric name."""
        if "execution_time" in metric_name:
            return AnomalyType.PERFORMANCE
        elif "success_rate" in metric_name or "quality_score" in metric_name:
            return AnomalyType.QUALITY
        elif "resource" in metric_name:
            return AnomalyType.USAGE
        else:
            return AnomalyType.PERFORMANCE
    
    def _get_suggested_actions(self, metric_name: str, z_score: float) -> List[str]:
        """Get suggested actions for anomaly."""
        actions = []
        
        if "execution_time" in metric_name:
            actions.extend([
                "Check for resource contention",
                "Review recent code changes",
                "Monitor system resource usage",
                "Consider scaling resources"
            ])
        elif "success_rate" in metric_name:
            actions.extend([
                "Review error logs",
                "Check input data quality",
                "Validate dependencies",
                "Test error handling"
            ])
        elif "quality_score" in metric_name:
            actions.extend([
                "Review code quality metrics",
                "Check documentation completeness",
                "Validate test coverage",
                "Review security practices"
            ])
        
        return actions[:3]  # Limit to 3 actions

class SkillRecommender:
    """Intelligent skill recommendation system."""
    
    def __init__(self):
        self.skill_profiles = {}
        self.usage_patterns = defaultdict(list)
        self.similarity_matrix = {}
        
    def update_skill_profile(self, skill_id: str, metrics: Dict[str, float], context: Dict[str, Any]):
        """Update skill profile for recommendations."""
        if skill_id not in self.skill_profiles:
            self.skill_profiles[skill_id] = {
                "performance_history": [],
                "quality_history": [],
                "usage_contexts": [],
                "success_patterns": [],
                "resource_patterns": []
            }
        
        profile = self.skill_profiles[skill_id]
        
        # Update histories
        profile["performance_history"].append(metrics.get("execution_time", 0))
        profile["quality_history"].append(metrics.get("quality_score", 0))
        profile["usage_contexts"].append(context)
        
        # Keep only recent data
        for key in ["performance_history", "quality_history"]:
            if len(profile[key]) > 100:
                profile[key] = profile[key][-100:]
        
        if len(profile["usage_contexts"]) > 100:
            profile["usage_contexts"] = profile["usage_contexts"][-100:]
    
    def recommend_skills(self, task_description: str, context: Dict[str, Any], 
                        available_skills: List[str]) -> List[SkillRecommendation]:
        """Recommend skills for a given task."""
        recommendations = []
        
        # Calculate skill scores based on various factors
        skill_scores = {}
        
        for skill_id in available_skills:
            score = self._calculate_skill_score(skill_id, task_description, context)
            skill_scores[skill_id] = score
        
        # Sort by score and create recommendations
        sorted_skills = sorted(skill_scores.items(), key=lambda x: x[1], reverse=True)
        
        for _i, (skill_id, score) in enumerate(sorted_skills[:5]):  # Top 5 recommendations
            recommendation = SkillRecommendation(
                recommendation_id=f"rec_{skill_id}_{datetime.now().isoformat()}",
                recommendation_type=RecommendationType.SKILL_SELECTION,
                skill_id=skill_id,
                confidence_score=score,
                description=f"Recommended skill for task: {task_description[:50]}...",
                actions=self._get_recommendation_actions(skill_id, score),
                expected_impact={
                    "performance_improvement": self._estimate_performance_improvement(skill_id),
                    "success_rate": self._estimate_success_rate(skill_id),
                    "resource_efficiency": self._estimate_resource_efficiency(skill_id)
                },
                timestamp=datetime.now()
            )
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _calculate_skill_score(self, skill_id: str, task_description: str, context: Dict[str, Any]) -> float:
        """Calculate recommendation score for a skill."""
        profile = self.skill_profiles.get(skill_id, {})
        
        if not profile:
            return 0.1  # Low score for unknown skills
        
        score = 0.5  # Base score
        
        # Performance factor
        if profile["performance_history"]:
            avg_performance = statistics.mean(profile["performance_history"])
            performance_factor = max(0, 1 - (avg_performance / 10.0))  # Normalize to 0-1
            score += performance_factor * 0.2
        
        # Quality factor
        if profile["quality_history"]:
            avg_quality = statistics.mean(profile["quality_history"])
            score += avg_quality * 0.2
        
        # Context matching
        context_factor = self._calculate_context_match(profile["usage_contexts"], context)
        score += context_factor * 0.3
        
        # Task description matching (simplified)
        task_keywords = task_description.lower().split()
        context_keywords = str(context).lower().split()
        matching_keywords = set(task_keywords) & set(context_keywords)
        task_match_factor = len(matching_keywords) / max(1, len(task_keywords))
        score += task_match_factor * 0.2
        
        return min(1.0, score)  # Cap at 1.0
    
    def _calculate_context_match(self, usage_contexts: List[Dict[str, Any]], 
                                current_context: Dict[str, Any]) -> float:
        """Calculate how well a skill matches the current context."""
        if not usage_contexts:
            return 0.0
        
        matches = 0
        total_comparisons = 0
        
        for past_context in usage_contexts[-10:]:  # Check last 10 contexts
            for key, value in current_context.items():
                if key in past_context:
                    total_comparisons += 1
                    if past_context[key] == value:
                        matches += 1
        
        return matches / max(1, total_comparisons)
    
    def _get_recommendation_actions(self, skill_id: str, score: float) -> List[str]:
        """Get recommended actions for a skill."""
        actions = []
        
        if score > 0.8:
            actions.append("Use this skill immediately")
            actions.append("Monitor performance closely")
        elif score > 0.6:
            actions.append("Consider this skill as primary option")
            actions.append("Test with sample data first")
        else:
            actions.append("Use this skill as backup option")
            actions.append("Monitor for potential issues")
        
        return actions
    
    def _estimate_performance_improvement(self, skill_id: str) -> float:
        """Estimate performance improvement percentage."""
        profile = self.skill_profiles.get(skill_id, {})
        if not profile.get("performance_history"):
            return 0.0
        
        recent_performance = statistics.mean(profile["performance_history"][-10:])
        historical_performance = statistics.mean(profile["performance_history"])
        
        if historical_performance == 0:
            return 0.0
        
        improvement = (historical_performance - recent_performance) / historical_performance
        return max(-0.5, min(0.5, improvement))  # Clamp between -50% and +50%
    
    def _estimate_success_rate(self, skill_id: str) -> float:
        """Estimate success rate for the skill."""
        profile = self.skill_profiles.get(skill_id, {})
        if not profile.get("quality_history"):
            return 0.5
        
        return statistics.mean(profile["quality_history"])
    
    def _estimate_resource_efficiency(self, skill_id: str) -> float:
        """Estimate resource efficiency."""
        profile = self.skill_profiles.get(skill_id, {})
        if not profile.get("performance_history"):
            return 0.5
        
        performance = statistics.mean(profile["performance_history"])
        return max(0.0, 1.0 - (performance / 10.0))  # Normalize to 0-1

class AdvancedAnalyticsEngine:
    """Main engine for advanced analytics and ML integration."""
    
    def __init__(self, model_path: Path):
        self.model_path = model_path
        self.performance_predictor = PerformancePredictor(model_path)
        self.anomaly_detector = AnomalyDetector()
        self.skill_recommender = SkillRecommender()
        
        # Analytics configuration
        self.prediction_horizon = 24  # hours
        self.anomaly_threshold = 0.1
        self.recommendation_cache = {}
        
    async def analyze_skill_performance(self, skill_id: str, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Perform comprehensive performance analysis."""
        analysis = {
            "skill_id": skill_id,
            "timestamp": datetime.now().isoformat(),
            "predictions": [],
            "anomalies": [],
            "recommendations": []
        }
        
        # Update training data
        self.performance_predictor.collect_training_data(skill_id, metrics)
        
        # Train model if needed
        if len(self.performance_predictor.performance_history[skill_id]) > 50:
            self.performance_predictor.train_performance_model(skill_id)
        
        # Generate predictions
        prediction = self.performance_predictor.predict_performance(skill_id, self.prediction_horizon)
        if prediction:
            analysis["predictions"].append(prediction)
        
        # Detect anomalies
        anomalies = self.anomaly_detector.detect_anomalies(skill_id, metrics)
        analysis["anomalies"] = anomalies
        
        # Update skill profile
        context = {"time_of_day": datetime.now().hour, "day_of_week": datetime.now().weekday()}
        self.skill_recommender.update_skill_profile(skill_id, metrics, context)
        
        return analysis
    
    async def generate_skill_recommendations(self, task_description: str, context: Dict[str, Any], 
                                           available_skills: List[str]) -> List[SkillRecommendation]:
        """Generate intelligent skill recommendations."""
        return self.skill_recommender.recommend_skills(task_description, context, available_skills)
    
    async def get_anomaly_summary(self, time_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """Get summary of detected anomalies."""
        relevant_anomalies = [
            a for a in self.anomaly_detector.anomalies
            if time_range[0] <= a.timestamp <= time_range[1]
        ]
        
        summary = {
            "total_anomalies": len(relevant_anomalies),
            "by_type": defaultdict(int),
            "by_severity": defaultdict(int),
            "by_skill": defaultdict(int),
            "recent_anomalies": relevant_anomalies[-10:]
        }
        
        for anomaly in relevant_anomalies:
            summary["by_type"][anomaly.anomaly_type.value] += 1
            summary["by_severity"][anomaly.severity] += 1
            summary["by_skill"][anomaly.skill_id] += 1
        
        return summary
    
    async def get_performance_insights(self, skill_id: str, days: int = 7) -> Dict[str, Any]:
        """Get performance insights and trends."""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        # Get historical data
        history = list(self.performance_predictor.performance_history[skill_id])
        if not history:
            return {"error": "No historical data available"}
        
        # Filter by time range
        filtered_history = [
            h for h in history
            if start_time <= datetime.fromisoformat(h["timestamp"]) <= end_time
        ]
        
        if not filtered_history:
            return {"error": "No data in specified time range"}
        
        # Calculate insights
        execution_times = [h["execution_time"] for h in filtered_history]
        
        insights = {
            "skill_id": skill_id,
            "time_range": {"start": start_time.isoformat(), "end": end_time.isoformat()},
            "basic_stats": {
                "avg_execution_time": statistics.mean(execution_times),
                "min_execution_time": min(execution_times),
                "max_execution_time": max(execution_times),
                "std_execution_time": statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
                "total_executions": len(execution_times)
            },
            "trends": self._calculate_trends(execution_times),
            "performance_ranking": self._calculate_performance_ranking(skill_id),
            "optimization_opportunities": self._identify_optimization_opportunities(execution_times)
        }
        
        return insights
    
    def _calculate_trends(self, execution_times: List[float]) -> Dict[str, Any]:
        """Calculate performance trends."""
        if len(execution_times) < 10:
            return {"error": "Insufficient data for trend analysis"}
        
        # Simple linear trend
        x = list(range(len(execution_times)))
        y = execution_times
        
        # Calculate trend line
        n = len(x)
        x_mean = statistics.mean(x)
        y_mean = statistics.mean(y)
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        
        return {
            "trend_direction": "improving" if slope < 0 else "degrading" if slope > 0 else "stable",
            "trend_slope": slope,
            "trend_strength": abs(slope) / (y_mean if y_mean != 0 else 1)
        }
    
    def _calculate_performance_ranking(self, skill_id: str) -> Dict[str, Any]:
        """Calculate performance ranking compared to other skills."""
        all_skills = list(self.performance_predictor.performance_history.keys())
        
        if len(all_skills) < 2:
            return {"ranking": 1, "total_skills": 1}
        
        # Calculate average performance for all skills
        skill_averages = {}
        for skill in all_skills:
            history = list(self.performance_predictor.performance_history[skill])
            if history:
                avg_time = statistics.mean([h["execution_time"] for h in history])
                skill_averages[skill] = avg_time
        
        if skill_id not in skill_averages:
            return {"ranking": len(all_skills), "total_skills": len(all_skills)}
        
        # Rank skills by performance (lower is better)
        sorted_skills = sorted(skill_averages.items(), key=lambda x: x[1])
        ranking = next(i for i, (skill, _) in enumerate(sorted_skills, 1) if skill == skill_id)
        
        return {
            "ranking": ranking,
            "total_skills": len(all_skills),
            "percentile": (len(all_skills) - ranking + 1) / len(all_skills) * 100
        }
    
    def _identify_optimization_opportunities(self, execution_times: List[float]) -> List[str]:
        """Identify potential optimization opportunities."""
        opportunities = []
        
        if len(execution_times) < 10:
            return opportunities
        
        avg_time = statistics.mean(execution_times)
        std_time = statistics.stdev(execution_times)
        
        # High execution time
        if avg_time > 5.0:
            opportunities.append("Consider optimizing algorithm efficiency")
        
        # High variance
        if std_time > avg_time * 0.5:
            opportunities.append("Investigate performance inconsistency causes")
        
        # Trend analysis
        recent_avg = statistics.mean(execution_times[-10:])
        earlier_avg = statistics.mean(execution_times[:10])
        
        if recent_avg > earlier_avg * 1.2:
            opportunities.append("Performance degradation detected - review recent changes")
        
        return opportunities

# Global advanced analytics instance
global_advanced_analytics = AdvancedAnalyticsEngine(Path("models"))

async def analyze_skill_performance(skill_id: str, metrics: Dict[str, float]) -> Dict[str, Any]:
    """Analyze skill performance using advanced analytics."""
    return await global_advanced_analytics.analyze_skill_performance(skill_id, metrics)

async def generate_skill_recommendations(task_description: str, context: Dict[str, Any], 
                                       available_skills: List[str]) -> List[SkillRecommendation]:
    """Generate intelligent skill recommendations."""
    return await global_advanced_analytics.generate_skill_recommendations(task_description, context, available_skills)

async def get_anomaly_summary(time_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
    """Get summary of detected anomalies."""
    return await global_advanced_analytics.get_anomaly_summary(time_range)

async def get_performance_insights(skill_id: str, days: int = 7) -> Dict[str, Any]:
    """Get performance insights and trends."""
    return await global_advanced_analytics.get_performance_insights(skill_id, days)

if __name__ == "__main__":
    # Example usage
    async def main():
        print("Advanced Analytics System Examples")
        
        # Test performance prediction
        metrics = {
            "execution_time": 2.5,
            "success_rate": 0.95,
            "quality_score": 0.85,
            "resource_usage": 0.6
        }
        
        analysis = await analyze_skill_performance("test_skill", metrics)
        print(f"Analysis completed: {len(analysis['predictions'])} predictions, {len(analysis['anomalies'])} anomalies")
        
        # Test skill recommendations
        recommendations = await generate_skill_recommendations(
            "Research AI agent orchestration",
            {"user_id": "test_user", "time_of_day": 14},
            ["skill1", "skill2", "skill3"]
        )
        print(f"Generated {len(recommendations)} recommendations")
        
        print("Advanced Analytics system working correctly")
    
    asyncio.run(main())
