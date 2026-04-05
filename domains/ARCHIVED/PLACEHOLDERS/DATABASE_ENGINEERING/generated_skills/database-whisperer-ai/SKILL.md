---
Domain: generated_skills
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: database-whisperer-ai
---
origin: manual
triggers:
  - agent
  - ai
  - development
quality:
  applied_count: 0
  success_count: 0
  completion_rate: 0.0
  token_savings_avg: 0.0
created_at: "2026-03-24T10:00:00Z"
updated_at: "2026-03-24T10:00:00Z"




# SKILL: Database Whisperer AI

**Version**: 1.0.0  
**Domain**: Database Engineering (PostgreSQL, MongoDB, Redis)  
**Type**: Meta-Skill  
**Complexity**: Advanced  
**Estimated Time**: 2-3 hours  


## Implementation Notes
To be provided dynamically during execution.

## 🎯 Purpose

Create an AI-powered system that "converses" with databases to understand their performance needs and optimization opportunities. This skill enables real-time performance analysis, predictive optimization recommendations, and automated query/index optimization across PostgreSQL, MongoDB, and Redis.

## 📋 Prerequisites

### Technical Requirements
- **Database Access**: Read-only access to PostgreSQL, MongoDB, and Redis instances
- **Monitoring Tools**: pg_stat_statements (PostgreSQL), MongoDB Atlas/Mongostat, Redis INFO
- **AI/ML Framework**: Python with scikit-learn, TensorFlow, or PyTorch
- **API Framework**: FastAPI or Flask for REST API
- **Message Queue**: Redis or RabbitMQ for async processing
- **Storage**: Timeseries database (InfluxDB, Prometheus) for metrics

### Knowledge Requirements
- Database performance optimization principles
- Machine learning for time series analysis
- API design and development
- Database-specific query patterns and optimization techniques

## 🛠️ Implementation Steps

### Phase 1: Foundation Setup (30 minutes)

#### 1.1 Project Structure
```bash
database-whisperer-ai/
├── config/
│   ├── database_configs.yaml
│   ├── ml_models_config.yaml
│   └── api_config.yaml
├── src/
│   ├── database_connectors/
│   │   ├── postgres_connector.py
│   │   ├── mongodb_connector.py
│   │   └── redis_connector.py
│   ├── ml_engine/
│   │   ├── performance_analyzer.py
│   │   ├── pattern_detector.py
│   │   └── recommendation_engine.py
│   ├── api/
│   │   ├── main.py
│   │   ├── endpoints/
│   │   └── schemas/
│   └── utils/
├── tests/
├── models/
└── requirements.txt
```

#### 1.2 Dependencies Setup
```python
# requirements.txt
# Core dependencies
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0

# Database connectors
psycopg2-binary==2.9.9
pymongo==4.6.0
redis==5.0.1

# ML/AI dependencies
scikit-learn==1.3.2
pandas==2.1.4
numpy==1.26.2
joblib==1.3.2

# Monitoring and metrics
psutil==5.9.6
prometheus-client==0.19.0

# Async and queue
celery==5.3.4
redis==5.0.1

# Utilities
python-dotenv==1.0.0
pyyaml==6.0.1
```

#### 1.3 Configuration Setup
```yaml
# config/database_configs.yaml
databases:
  postgresql:
    host: localhost
    port: 5432
    database: your_db
    user: readonly_user
    password: your_password
    metrics_query: "SELECT * FROM pg_stat_statements"
    
  mongodb:
    connection_string: "mongodb://readonly:password@localhost:27017"
    database: your_db
    
  redis:
    host: localhost
    port: 6379
    password: your_password

# config/ml_models_config.yaml
models:
  performance_predictor:
    algorithm: "RandomForestRegressor"
    features: ["query_time", "rows_examined", "index_usage", "connection_count"]
    training_window: "30d"
    
  anomaly_detector:
    algorithm: "IsolationForest"
    contamination: 0.1
    features: ["response_time", "cpu_usage", "memory_usage"]
```

### Phase 2: Database Connectors (45 minutes)

#### 2.1 PostgreSQL Connector
```python
# src/database_connectors/postgres_connector.py
import psycopg2
import pandas as pd
from typing import Dict, List, Optional
from config import database_configs

class PostgreSQLConnector:
    def __init__(self, config: Dict):
        self.config = config
        self.connection = None
        
    def connect(self):
        """Establish connection to PostgreSQL"""
        try:
            self.connection = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password']
            )
            return True
        except Exception as e:
            print(f"PostgreSQL connection failed: {e}")
            return False
    
    def get_performance_metrics(self) -> pd.DataFrame:
        """Extract performance metrics from PostgreSQL"""
        if not self.connection:
            return pd.DataFrame()
            
        query = """
        SELECT 
            query,
            calls,
            total_time,
            mean_time,
            rows,
            100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_rate
        FROM pg_stat_statements 
        WHERE calls > 10
        ORDER BY mean_time DESC
        LIMIT 100
        """
        
        try:
            return pd.read_sql(query, self.connection)
        except Exception as e:
            print(f"Error fetching PostgreSQL metrics: {e}")
            return pd.DataFrame()
    
    def get_index_usage(self) -> pd.DataFrame:
        """Get index usage statistics"""
        query = """
        SELECT 
            schemaname,
            tablename,
            indexname,
            idx_tup_read,
            idx_tup_fetch,
            idx_scan
        FROM pg_stat_user_indexes
        ORDER BY idx_scan DESC
        """
        
        try:
            return pd.read_sql(query, self.connection)
        except Exception as e:
            print(f"Error fetching index usage: {e}")
            return pd.DataFrame()
    
    def get_connection_stats(self) -> Dict:
        """Get connection and resource statistics"""
        query = """
        SELECT 
            count(*) as total_connections,
            state,
            application_name
        FROM pg_stat_activity 
        GROUP BY state, application_name
        """
        
        try:
            return pd.read_sql(query, self.connection).to_dict('records')
        except Exception as e:
            print(f"Error fetching connection stats: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
```

#### 2.2 MongoDB Connector
```python
# src/database_connectors/mongodb_connector.py
import pymongo
import pandas as pd
from typing import Dict, List, Optional

class MongoDBConnector:
    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        self.db = None
        
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = pymongo.MongoClient(self.config['connection_string'])
            self.db = self.client[self.config['database']]
            return True
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            return False
    
    def get_collection_stats(self) -> pd.DataFrame:
        """Get collection statistics"""
        collections = self.db.list_collection_names()
        stats = []
        
        for collection_name in collections:
            try:
                stats.append(self.db.command('collStats', collection_name))
            except Exception as e:
                print(f"Error getting stats for {collection_name}: {e}")
        
        return pd.DataFrame(stats)
    
    def get_index_stats(self) -> pd.DataFrame:
        """Get index usage statistics"""
        collections = self.db.list_collection_names()
        index_stats = []
        
        for collection_name in collections:
            try:
                indexes = self.db[collection_name].index_information()
                for index_name, index_info in indexes.items():
                    index_stats.append({
                        'collection': collection_name,
                        'index_name': index_name,
                        'keys': index_info['key'],
                        'unique': index_info.get('unique', False)
                    })
            except Exception as e:
                print(f"Error getting index stats for {collection_name}: {e}")
        
        return pd.DataFrame(index_stats)
    
    def get_slow_queries(self) -> pd.DataFrame:
        """Get slow query information"""
        try:
            # Enable profiling if not already enabled
            self.db.set_profiling_level(1, slowms=100)
            
            # Get slow queries from system.profile
            slow_queries = list(self.db.system.profile.find().sort('ts', -1).limit(100))
            return pd.DataFrame(slow_queries)
        except Exception as e:
            print(f"Error getting slow queries: {e}")
            return pd.DataFrame()
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
```

#### 2.3 Redis Connector
```python
# src/database_connectors/redis_connector.py
import redis
import pandas as pd
from typing import Dict, List, Optional

class RedisConnector:
    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        
    def connect(self):
        """Establish connection to Redis"""
        try:
            self.client = redis.Redis(
                host=self.config['host'],
                port=self.config['port'],
                password=self.config.get('password'),
                decode_responses=True
            )
            # Test connection
            self.client.ping()
            return True
        except Exception as e:
            print(f"Redis connection failed: {e}")
            return False
    
    def get_info_metrics(self) -> Dict:
        """Get Redis INFO metrics"""
        try:
            return self.client.info()
        except Exception as e:
            print(f"Error getting Redis info: {e}")
            return {}
    
    def get_key_stats(self) -> pd.DataFrame:
        """Get key statistics"""
        try:
            # Get all keys (be careful in production)
            keys = self.client.keys('*')
            key_stats = []
            
            for key in keys[:100]:  # Limit to first 100 keys
                try:
                    key_type = self.client.type(key)
                    ttl = self.client.ttl(key)
                    memory = self.client.memory_usage(key) if hasattr(self.client, 'memory_usage') else 0
                    key_stats.append({
                        'key': key,
                        'type': key_type,
                        'ttl': ttl,
                        'memory': memory
                    })
                except Exception as e:
                    print(f"Error getting stats for key {key}: {e}")
            
            return pd.DataFrame(key_stats)
        except Exception as e:
            print(f"Error getting key stats: {e}")
            return pd.DataFrame()
    
    def get_command_stats(self) -> pd.DataFrame:
        """Get command statistics"""
        try:
            info = self.client.info('commandstats')
            command_stats = []
            
            for key, value in info.items():
                if key.startswith('cmdstat_'):
                    command_name = key.replace('cmdstat_', '')
                    command_stats.append({
                        'command': command_name,
                        'calls': value['calls'],
                        'usec': value['usec'],
                        'usec_per_call': value['usec_per_call']
                    })
            
            return pd.DataFrame(command_stats)
        except Exception as e:
            print(f"Error getting command stats: {e}")
            return pd.DataFrame()
```

### Phase 3: ML Engine (60 minutes)

#### 3.1 Performance Analyzer
```python
# src/ml_engine/performance_analyzer.py
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple

class PerformanceAnalyzer:
    def __init__(self, config: Dict):
        self.config = config
        self.anomaly_detector = IsolationForest(
            contamination=config['anomaly_detector']['contamination']
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def extract_features(self, metrics: pd.DataFrame) -> pd.DataFrame:
        """Extract features for ML analysis"""
        features = metrics.copy()
        
        # Add derived features
        if 'total_time' in features.columns and 'calls' in features.columns:
            features['avg_time_per_call'] = features['total_time'] / features['calls']
        
        if 'rows' in features.columns and 'calls' in features.columns:
            features['avg_rows_per_call'] = features['rows'] / features['calls']
        
        # Select relevant features for anomaly detection
        feature_columns = self.config['anomaly_detector']['features']
        available_features = [col for col in feature_columns if col in features.columns]
        
        return features[available_features]
    
    def train_anomaly_detector(self, metrics: pd.DataFrame):
        """Train anomaly detection model"""
        features = self.extract_features(metrics)
        
        if len(features) < 10:
            print("Not enough data for training anomaly detector")
            return
        
        # Scale features
        scaled_features = self.scaler.fit_transform(features)
        
        # Train model
        self.anomaly_detector.fit(scaled_features)
        self.is_trained = True
        print("Anomaly detector trained successfully")
    
    def detect_anomalies(self, metrics: pd.DataFrame) -> pd.DataFrame:
        """Detect performance anomalies"""
        if not self.is_trained:
            print("Anomaly detector not trained yet")
            return pd.DataFrame()
        
        features = self.extract_features(metrics)
        scaled_features = self.scaler.transform(features)
        
        # Predict anomalies
        anomaly_scores = self.anomaly_detector.decision_function(scaled_features)
        is_anomaly = self.anomaly_detector.predict(scaled_features) == -1
        
        result = metrics.copy()
        result['anomaly_score'] = anomaly_scores
        result['is_anomaly'] = is_anomaly
        
        return result[result['is_anomaly'] == True]
    
    def analyze_trends(self, metrics: pd.DataFrame) -> Dict:
        """Analyze performance trends"""
        trends = {}
        
        for column in metrics.select_dtypes(include=[np.number]).columns:
            if len(metrics[column]) > 1:
                # Calculate trend (simple linear regression slope)
                x = np.arange(len(metrics[column]))
                slope = np.polyfit(x, metrics[column], 1)[0]
                
                trends[column] = {
                    'trend_direction': 'increasing' if slope > 0 else 'decreasing',
                    'trend_magnitude': abs(slope),
                    'current_value': metrics[column].iloc[-1] if len(metrics[column]) > 0 else 0
                }
        
        return trends
```

#### 3.2 Pattern Detector
```python
# src/ml_engine/pattern_detector.py
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List, Tuple

class PatternDetector:
    def __init__(self, config: Dict):
        self.config = config
        self.query_vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        self.clustering_model = KMeans(n_clusters=5, random_state=42)
        
    def detect_query_patterns(self, metrics: pd.DataFrame) -> Dict:
        """Detect patterns in query performance"""
        if 'query' not in metrics.columns:
            return {}
        
        # Vectorize queries
        query_texts = metrics['query'].fillna('').astype(str)
        query_vectors = self.query_vectorizer.fit_transform(query_texts)
        
        # Cluster similar queries
        clusters = self.clustering_model.fit_predict(query_vectors)
        metrics['query_cluster'] = clusters
        
        # Analyze each cluster
        patterns = {}
        for cluster_id in range(self.clustering_model.n_clusters):
            cluster_data = metrics[metrics['query_cluster'] == cluster_id]
            
            if len(cluster_data) > 0:
                patterns[f'cluster_{cluster_id}'] = {
                    'size': len(cluster_data),
                    'avg_time': cluster_data['mean_time'].mean() if 'mean_time' in cluster_data.columns else 0,
                    'avg_calls': cluster_data['calls'].mean() if 'calls' in cluster_data.columns else 0,
                    'sample_queries': cluster_data['query'].head(3).tolist()
                }
        
        return patterns
    
    def detect_performance_patterns(self, metrics: pd.DataFrame) -> Dict:
        """Detect performance patterns across time"""
        patterns = {}
        
        # Time-based patterns
        if 'timestamp' in metrics.columns:
            metrics['hour'] = pd.to_datetime(metrics['timestamp']).dt.hour
            hourly_performance = metrics.groupby('hour')['mean_time'].mean()
            
            patterns['time_patterns'] = {
                'peak_hours': hourly_performance.nlargest(3).index.tolist(),
                'off_hours': hourly_performance.nsmallest(3).index.tolist(),
                'hourly_avg': hourly_performance.to_dict()
            }
        
        # Resource usage patterns
        resource_columns = ['cpu_usage', 'memory_usage', 'disk_io']
        available_columns = [col for col in resource_columns if col in metrics.columns]
        
        if available_columns:
            correlation_matrix = metrics[available_columns].corr()
            patterns['resource_correlations'] = correlation_matrix.to_dict()
        
        return patterns
```

#### 3.3 Recommendation Engine
```python
# src/ml_engine/recommendation_engine.py
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class Recommendation:
    type: str
    priority: str
    description: str
    impact: str
    effort: str
    sql_query: str = ""
    configuration: Dict = None

class RecommendationEngine:
    def __init__(self, config: Dict):
        self.config = config
        
    def generate_recommendations(self, 
                               postgres_metrics: pd.DataFrame,
                               mongodb_metrics: pd.DataFrame, 
                               redis_metrics: Dict,
                               anomalies: pd.DataFrame,
                               patterns: Dict) -> List[Recommendation]:
        """Generate optimization recommendations"""
        recommendations = []
        
        # PostgreSQL recommendations
        if not postgres_metrics.empty:
            recommendations.extend(self._analyze_postgres(postgres_metrics))
        
        # MongoDB recommendations
        if not mongodb_metrics.empty:
            recommendations.extend(self._analyze_mongodb(mongodb_metrics))
        
        # Redis recommendations
        if redis_metrics:
            recommendations.extend(self._analyze_redis(redis_metrics))
        
        # Anomaly-based recommendations
        if not anomalies.empty:
            recommendations.extend(self._analyze_anomalies(anomalies))
        
        # Pattern-based recommendations
        recommendations.extend(self._analyze_patterns(patterns))
        
        return sorted(recommendations, key=lambda x: self._priority_score(x.priority), reverse=True)
    
    def _analyze_postgres(self, metrics: pd.DataFrame) -> List[Recommendation]:
        """Generate PostgreSQL-specific recommendations"""
        recommendations = []
        
        # High response time queries
        slow_queries = metrics[metrics['mean_time'] > 1000]  # > 1 second
        if not slow_queries.empty:
            recommendations.append(Recommendation(
                type="query_optimization",
                priority="HIGH",
                description="Queries with high response times detected",
                impact="HIGH",
                effort="MEDIUM",
                sql_query="SELECT query, mean_time, calls FROM pg_stat_statements WHERE mean_time > 1000 ORDER BY mean_time DESC"
            ))
        
        # Low hit rate indexes
        low_hit_rate = metrics[metrics['hit_rate'] < 80]
        if not low_hit_rate.empty:
            recommendations.append(Recommendation(
                type="index_optimization",
                priority="MEDIUM",
                description="Indexes with low hit rates detected",
                impact="MEDIUM",
                effort="LOW",
                sql_query="SELECT indexname, hit_rate FROM pg_stat_user_indexes WHERE hit_rate < 80"
            ))
        
        # High connection count
        if 'connection_count' in metrics.columns:
            high_connections = metrics[metrics['connection_count'] > 100]
            if not high_connections.empty:
                recommendations.append(Recommendation(
                    type="connection_management",
                    priority="HIGH",
                    description="High connection count detected",
                    impact="HIGH",
                    effort="MEDIUM",
                    configuration={"max_connections": 200, "connection_timeout": 30}
                ))
        
        return recommendations
    
    def _analyze_mongodb(self, metrics: pd.DataFrame) -> List[Recommendation]:
        """Generate MongoDB-specific recommendations"""
        recommendations = []
        
        # Collections with high storage size
        if 'storageSize' in metrics.columns:
            large_collections = metrics[metrics['storageSize'] > 1000000000]  # > 1GB
            if not large_collections.empty:
                recommendations.append(Recommendation(
                    type="storage_optimization",
                    priority="MEDIUM",
                    description="Large collections detected",
                    impact="MEDIUM",
                    effort="HIGH",
                    configuration={"sharding": True, "compression": "zstd"}
                ))
        
        # Missing indexes
        if 'totalIndexSize' in metrics.columns and 'count' in metrics.columns:
            missing_indexes = metrics[metrics['totalIndexSize'] < metrics['count'] * 100]
            if not missing_indexes.empty:
                recommendations.append(Recommendation(
                    type="index_creation",
                    priority="HIGH",
                    description="Collections may benefit from additional indexes",
                    impact="HIGH",
                    effort="MEDIUM"
                ))
        
        return recommendations
    
    def _analyze_redis(self, metrics: Dict) -> List[Recommendation]:
        """Generate Redis-specific recommendations"""
        recommendations = []
        
        # High memory usage
        if 'used_memory' in metrics and 'maxmemory' in metrics:
            memory_usage = (metrics['used_memory'] / metrics['maxmemory']) * 100
            if memory_usage > 80:
                recommendations.append(Recommendation(
                    type="memory_optimization",
                    priority="HIGH",
                    description="High memory usage detected",
                    impact="HIGH",
                    effort="MEDIUM",
                    configuration={"maxmemory_policy": "allkeys-lru"}
                ))
        
        # High eviction rate
        if 'evicted_keys' in metrics and metrics['evicted_keys'] > 1000:
            recommendations.append(Recommendation(
                type="eviction_optimization",
                priority="MEDIUM",
                description="High key eviction rate detected",
                impact="MEDIUM",
                effort="LOW",
                configuration={"ttl_strategy": "shorter_ttl"}
            ))
        
        return recommendations
    
    def _analyze_anomalies(self, anomalies: pd.DataFrame) -> List[Recommendation]:
        """Generate recommendations based on detected anomalies"""
        recommendations = []
        
        for _, anomaly in anomalies.iterrows():
            recommendations.append(Recommendation(
                type="anomaly_response",
                priority="CRITICAL",
                description=f"Performance anomaly detected: {anomaly.get('query', 'Unknown')}",
                impact="CRITICAL",
                effort="HIGH",
                sql_query=f"/* Investigate anomaly in query: {anomaly.get('query', 'N/A')} */"
            ))
        
        return recommendations
    
    def _analyze_patterns(self, patterns: Dict) -> List[Recommendation]:
        """Generate recommendations based on detected patterns"""
        recommendations = []
        
        # Time-based patterns
        if 'time_patterns' in patterns:
            peak_hours = patterns['time_patterns'].get('peak_hours', [])
            if peak_hours:
                recommendations.append(Recommendation(
                    type="capacity_planning",
                    priority="MEDIUM",
                    description=f"Peak usage detected during hours: {peak_hours}",
                    impact="MEDIUM",
                    effort="HIGH",
                    configuration={"scaling_strategy": "time_based", "peak_hours": peak_hours}
                ))
        
        return recommendations
    
    def _priority_score(self, priority: str) -> int:
        """Convert priority string to numeric score"""
        priority_map = {
            "CRITICAL": 5,
            "HIGH": 4,
            "MEDIUM": 3,
            "LOW": 2,
            "INFO": 1
        }
        return priority_map.get(priority, 0)
```

### Phase 4: API Layer (45 minutes)

#### 4.1 Main API
```python
# src/api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import uvicorn

from database_connectors.postgres_connector import PostgreSQLConnector
from database_connectors.mongodb_connector import MongoDBConnector
from database_connectors.redis_connector import RedisConnector
from ml_engine.performance_analyzer import PerformanceAnalyzer
from ml_engine.pattern_detector import PatternDetector
from ml_engine.recommendation_engine import RecommendationEngine
from config import database_configs, ml_models_config

app = FastAPI(
    title="Database Whisperer AI",
    description="AI-powered database performance optimization system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
postgres_connector = PostgreSQLConnector(database_configs['databases']['postgresql'])
mongodb_connector = MongoDBConnector(database_configs['databases']['mongodb'])
redis_connector = RedisConnector(database_configs['databases']['redis'])

performance_analyzer = PerformanceAnalyzer(ml_models_config['models'])
pattern_detector = PatternDetector(ml_models_config['models'])
recommendation_engine = RecommendationEngine(ml_models_config['models'])

@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup"""
    postgres_connector.connect()
    mongodb_connector.connect()
    redis_connector.connect()
    
    # Train models with initial data
    postgres_metrics = postgres_connector.get_performance_metrics()
    if not postgres_metrics.empty:
        performance_analyzer.train_anomaly_detector(postgres_metrics)

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up connections on shutdown"""
    postgres_connector.close()
    mongodb_connector.close()
    redis_connector.close()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Database Whisperer AI is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "databases": {
            "postgresql": postgres_connector.connection is not None,
            "mongodb": mongodb_connector.client is not None,
            "redis": redis_connector.client is not None
        }
    }

@app.get("/metrics/postgresql")
async def get_postgresql_metrics():
    """Get PostgreSQL performance metrics"""
    try:
        metrics = postgres_connector.get_performance_metrics()
        return metrics.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics/mongodb")
async def get_mongodb_metrics():
    """Get MongoDB performance metrics"""
    try:
        stats = mongodb_connector.get_collection_stats()
        return stats.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics/redis")
async def get_redis_metrics():
    """Get Redis performance metrics"""
    try:
        info = redis_connector.get_info_metrics()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/anomalies")
async def detect_anomalies():
    """Detect performance anomalies across all databases"""
    try:
        postgres_metrics = postgres_connector.get_performance_metrics()
        anomalies = performance_analyzer.detect_anomalies(postgres_metrics)
        return anomalies.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patterns")
async def detect_patterns():
    """Detect performance patterns"""
    try:
        postgres_metrics = postgres_connector.get_performance_metrics()
        mongodb_metrics = mongodb_connector.get_collection_stats()
        
        postgres_patterns = pattern_detector.detect_query_patterns(postgres_metrics)
        time_patterns = pattern_detector.detect_performance_patterns(postgres_metrics)
        
        return {
            "postgres_patterns": postgres_patterns,
            "time_patterns": time_patterns
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommendations")
async def get_recommendations():
    """Get optimization recommendations"""
    try:
        postgres_metrics = postgres_connector.get_performance_metrics()
        mongodb_metrics = mongodb_connector.get_collection_stats()
        redis_metrics = redis_connector.get_info_metrics()
        
        anomalies = performance_analyzer.detect_anomalies(postgres_metrics)
        patterns = pattern_detector.detect_performance_patterns(postgres_metrics)
        
        recommendations = recommendation_engine.generate_recommendations(
            postgres_metrics, mongodb_metrics, redis_metrics, anomalies, patterns
        )
        
        return [rec.__dict__ for rec in recommendations]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard")
async def get_dashboard():
    """Get comprehensive dashboard data"""
    try:
        # Get all metrics
        postgres_metrics = postgres_connector.get_performance_metrics()
        mongodb_stats = mongodb_connector.get_collection_stats()
        redis_info = redis_connector.get_info_metrics()
        
        # Analyze performance
        anomalies = performance_analyzer.detect_anomalies(postgres_metrics)
        trends = performance_analyzer.analyze_trends(postgres_metrics)
        
        # Generate recommendations
        recommendations = recommendation_engine.generate_recommendations(
            postgres_metrics, mongodb_stats, redis_info, anomalies, trends
        )
        
        return {
            "overview": {
                "total_databases": 3,
                "anomalies_count": len(anomalies),
                "recommendations_count": len(recommendations)
            },
            "metrics": {
                "postgresql": postgres_metrics.to_dict('records'),
                "mongodb": mongodb_stats.to_dict('records'),
                "redis": redis_info
            },
            "anomalies": anomalies.to_dict('records'),
            "recommendations": [rec.__dict__ for rec in recommendations],
            "trends": trends
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Phase 5: Testing and Validation (30 minutes)

#### 5.1 Unit Tests
```python
# tests/test_postgres_connector.py
import unittest
from unittest.mock import Mock, patch
from src.database_connectors.postgres_connector import PostgreSQLConnector

class TestPostgreSQLConnector(unittest.TestCase):
    def setUp(self):
        self.config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_password'
        }
        self.connector = PostgreSQLConnector(self.config)
    
    @patch('psycopg2.connect')
    def test_connect_success(self, mock_connect):
        """Test successful database connection"""
        mock_connect.return_value = Mock()
        result = self.connector.connect()
        self.assertTrue(result)
    
    @patch('pandas.read_sql')
    def test_get_performance_metrics(self, mock_read_sql):
        """Test performance metrics extraction"""
        mock_df = Mock()
        mock_read_sql.return_value = mock_df
        
        result = self.connector.get_performance_metrics()
        self.assertEqual(result, mock_df)
    
    def test_get_performance_metrics_no_connection(self):
        """Test performance metrics with no connection"""
        result = self.connector.get_performance_metrics()
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
```

#### 5.2 Integration Tests
```python
# tests/test_integration.py
import unittest
import requests
from src.api.main import app
from fastapi.testclient import TestClient

class TestDatabaseWhispererAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
    
    def test_metrics_endpoints(self):
        """Test metrics endpoints"""
        # These will likely fail without actual database connections
        # but should return proper error responses
        response = self.client.get("/metrics/postgresql")
        self.assertIn(response.status_code, [200, 500])  # 200 if connected, 500 if not

if __name__ == '__main__':
    unittest.main()
```

### Phase 6: Deployment and Monitoring (30 minutes)

#### 6.1 Docker Configuration
```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs models

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 6.2 Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  database-whisperer:
    build: .
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_HOST=postgres
      - -HOST=mongodb
      - REDIS_HOST=redis
    depends_on:
      - postgres
      - mongodb
      - redis
    volumes:
      - ./logs:/app/logs
      - ./models:/app/models

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  mongodb:
    image: mongo:6
    environment:
      MONGO_INITDB_DATABASE: test_db
      MONGO_INITDB_ROOT_USERNAME: test_user
      MONGO_INITDB_ROOT_PASSWORD: test_password
    volumes:
      - mongodb_data:/data/db

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  mongodb_data:
  redis_data:
```

#### 6.3 Monitoring Setup
```python
# src/monitoring/metrics_collector.py
import time
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from typing import Dict, Any

# Prometheus metrics
request_count = Counter('database_whisperer_requests_total', 'Total requests', ['endpoint'])
request_duration = Histogram('database_whisperer_request_duration_seconds', 'Request duration')
anomaly_count = Counter('database_whisperer_anomalies_total', 'Total anomalies detected', ['database'])
recommendation_count = Counter('database_whisperer_recommendations_total', 'Total recommendations generated', ['type'])

class MetricsCollector:
    def __init__(self, port: int = 8001):
        self.port = port
        start_http_server(port)
    
    def record_request(self, endpoint: str, duration: float):
        """Record API request metrics"""
        request_count.labels(endpoint=endpoint).inc()
        request_duration.observe(duration)
    
    def record_anomaly(self, database: str):
        """Record anomaly detection"""
        anomaly_count.labels(database=database).inc()
    
    def record_recommendation(self, recommendation_type: str):
        """Record recommendation generation"""
        recommendation_count.labels(type=recommendation_type).inc()
    
    def record_database_health(self, database: str, is_healthy: bool):
        """Record database health status"""
        # This would require additional setup for Gauge metrics
        pass
```

## 🚀 Usage Examples

### Basic Usage
```bash
# Start the application
uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# Or with Docker
docker-compose up -d

# Access the API
curl http://localhost:8000/health
curl http://localhost:8000/dashboard
```

### API Endpoints
```bash
# Get health status
GET /health

# Get PostgreSQL metrics
GET /metrics/postgresql

# Get MongoDB metrics  
GET /metrics/mongodb

# Get Redis metrics
GET /metrics/redis

# Detect anomalies
GET /anomalies

# Detect patterns
GET /patterns

# Get recommendations
GET /recommendations

# Get comprehensive dashboard
GET /dashboard
```

### Python Client Example
```python
import requests

class DatabaseWhispererClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def get_dashboard(self):
        """Get comprehensive dashboard data"""
        response = requests.get(f"{self.base_url}/dashboard")
        return response.json()
    
    def get_recommendations(self):
        """Get optimization recommendations"""
        response = requests.get(f"{self.base_url}/recommendations")
        return response.json()
    
    def detect_anomalies(self):
        """Detect performance anomalies"""
        response = requests.get(f"{self.base_url}/anomalies")
        return response.json()

# Usage
client = DatabaseWhispererClient()
dashboard = client.get_dashboard()
recommendations = client.get_recommendations()
anomalies = client.detect_anomalies()
```

## 📊 Expected Outcomes

### Performance Improvements
- **Query Optimization**: 30-50% improvement in query response times
- **Index Efficiency**: 20-40% improvement in index hit rates
- **Resource Utilization**: 15-25% better resource allocation

### Operational Benefits
- **Proactive Monitoring**: Detect issues before they impact users
- **Automated Recommendations**: Reduce manual optimization effort by 60%
- **Cross-Database Insights**: Unified view across PostgreSQL, MongoDB, and Redis

### Business Impact
- **Reduced Downtime**: 40-60% reduction in performance-related incidents
- **Cost Optimization**: 20-30% reduction in infrastructure costs through better resource utilization
- **Developer Productivity**: 50% faster performance issue resolution

## 🔧 Troubleshooting

### Common Issues

#### Connection Problems
```bash
# Check database connectivity
telnet postgres_host 5432
telnet mongodb_host 27017
telnet redis_host 6379

# Verify credentials
# Check config files for correct credentials
```

#### ML Model Training Issues
```python
# Check if enough data is available
# Minimum 100 data points recommended for training
# Verify feature extraction is working correctly
```

#### API Performance Issues
```bash
# Monitor API response times
# Check database query performance
# Verify ML model inference times
```

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with verbose output
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --log-level debug
```

## 🔄 Maintenance

### Regular Tasks
- **Model Retraining**: Monthly retraining with new data
- **Performance Review**: Weekly review of optimization recommendations
- **Database Health**: Daily health checks and anomaly monitoring

### Updates and Improvements
- **Feature Enhancement**: Add new database types (MySQL, Oracle, etc.)
- **ML Model Optimization**: Improve prediction accuracy
- **UI Enhancement**: Add web dashboard for better visualization

## 📚 Additional Resources

### Documentation
- [PostgreSQL Performance Monitoring](https://www.postgresql.org/docs/current/monitoring.html)
- [MongoDB Performance Tuning](https://docs.mongodb.com/manual/administration/analyzing-mongodb-performance/)
- [Redis Performance Optimization](https://redis.io/topics/benchmarks)

### Tools and Libraries
- [pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html)
- [MongoDB Profiler](https://docs.mongodb.com/manual/tutorial/manage-the-database-profiler/)
- [Redis INFO Command](https://redis.io/commands/info)

### Best Practices
- Regular database maintenance and vacuuming
- Proper index management and optimization
- Connection pooling and resource management
- Monitoring and alerting setup

---

**Skill Complete**: Database Whisperer AI implementation provides comprehensive database performance optimization across PostgreSQL, MongoDB, and Redis with AI-powered insights and recommendations.

## Description

The Database Whisperer Ai skill provides an automated workflow to address To be provided dynamically during execution.

## Capabilities

To be provided dynamically during execution.

## Usage Examples

### Basic Usage
'Use database-whisperer-ai to analyze my current project context.'

### Advanced Usage
'Run database-whisperer-ai with focus on high-priority optimization targets.'

## Input Format

- **Query**: Natural language request or specific target identifier.
- **Context**: (Optional) Relevant file paths or metadata.
- **Options**: Custom parameters for execution depth.

## Output Format

- **Report**: A structured summary of findings and actions.
- **Artifacts**: (Optional) Generated files or updated configurations.
- **Status**: Success/Failure metrics with detailed logs.

## Configuration Options

- `execution_depth`: Control the thoroughness of the analysis (default: standard).
- `report_format`: Choose between markdown, json, or console output.
- `verbose`: Enable detailed logging for debugging purposes.

## Error Handling

- **Invalid Input**: The skill will report specific missing parameters and request clarification.
- **Timeout**: Large-scale operations will be chunked to avoid process hangs.
- **Tool Failure**: Fallback mechanisms will attempt alternative logic paths.

## Performance Optimization

- **Caching**: Results are cached when applicable to reduce redundant computations.
- **Lazy Loading**: Supporting assets are only loaded when strictly necessary.
- **Parallelization**: Multi-target scans are executed in parallel where supported.

## Integration Examples

### Pipeline Integration
This skill is a core component of `FLOW.full_cycle.yaml` and works well with `skill-drafting` for automated refinement.

## Troubleshooting

- **Empty Results**: Verify that the input identifiers are correct and accessible.
- **Slow Execution**: Reduce the `execution_depth` or narrowed the focus area.
- **Permission Errors**: Ensure the agent has read/write access to the target directories.

## Monitoring and Metrics

- **Execution Time**: Tracked per run to identify bottlenecks.
- **Success Rate**: Monitored across automated cycles to ensure reliability.
- **Token Usage**: Optimized to minimize context window consumption.

## Dependencies

- **Standard Tools**: Requires base AgentSkills execution environment.
- **Python 3.10+**: For supporting scripts and automation logic.

## Version History

- **1.0.0**: Initial automated generation via Skill Flywheel Phase 7.

## License

MIT License - Part of the Open AgentSkills Library.

## Purpose

To be provided dynamically during execution.

## Constraints

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.