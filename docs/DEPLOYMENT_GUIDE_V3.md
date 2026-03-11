# Enhanced MCP Server v3 - Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the Enhanced MCP Server v3 with advanced dynamic lazy loading, ML-driven optimization, and container orchestration.

## Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows with WSL2
- **Python**: 3.11 or higher
- **Docker**: 20.10 or higher
- **Docker Compose**: 2.0 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 10GB available space

### Dependencies
- Redis for caching and Celery broker
- Prometheus for metrics collection
- Grafana for monitoring dashboards
- Docker for containerization

## Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd skill-flywheel

# Install Python dependencies
pip install -r requirements_v3.txt

# Create necessary directories
mkdir -p skills models logs monitoring/grafana/dashboards monitoring/grafana/datasources nginx/ssl
```

### 2. Configuration
```bash
# Copy and customize configuration
cp mcp_config.yaml.example mcp_config.yaml

# Edit configuration as needed
nano mcp_config.yaml
```

### 3. Docker Deployment
```bash
# Build and start all services
docker-compose -f docker-compose.v3.yml up -d

# Check service status
docker-compose -f docker-compose.v3.yml ps

# View logs
docker-compose -f docker-compose.v3.yml logs -f mcp-server-v3
```

### 4. Verification
```bash
# Check server health
curl http://localhost:8000/health

# Check Prometheus metrics
curl http://localhost:8001/metrics

# Access Grafana dashboard
open http://localhost:3000 (admin/admin)
```

## Detailed Deployment

### Local Development

#### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_v3.txt

# Set environment variables
export REDIS_URL=redis://localhost:6379/0
export CELERY_BROKER_URL=redis://localhost:6379/1
export CELERY_RESULT_BACKEND=redis://localhost:6379/2
```

#### 2. Local Services
```bash
# Start Redis
redis-server

# Start the server
python enhanced_mcp_server_v3.py

# In another terminal, start Celery worker
celery -A enhanced_mcp_server_v3.celery_app worker --loglevel=info

# Start Celery beat for scheduled tasks
celery -A enhanced_mcp_server_v3.celery_app beat --loglevel=info
```

#### 3. Testing
```bash
# Run tests
python test_enhanced_mcp_server_v3.py

# Run specific test categories
pytest test_enhanced_mcp_server_v3.py::TestServerConfig -v
pytest test_enhanced_mcp_server_v3.py::TestPerformance -v
```

### Production Deployment

#### 1. Docker Compose Production
```bash
# Create production configuration
cp docker-compose.v3.yml docker-compose.prod.yml

# Customize for production
# - Update image tags to specific versions
# - Configure SSL certificates
# - Set up proper logging
# - Configure resource limits
```

#### 2. Kubernetes Deployment
```bash
# Create Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

#### 3. Monitoring Setup
```bash
# Configure Prometheus alerts
cp monitoring/prometheus.yml.example monitoring/prometheus.yml
# Edit alert rules as needed

# Import Grafana dashboards
# - Access Grafana at http://localhost:3000
# - Import dashboard from monitoring/grafana/dashboards/
```

## Configuration Reference

### Server Configuration
```yaml
server:
  host: "0.0.0.0"
  port: 8000
  debug: false
  workers: 2
  max_concurrent_requests: 100
  request_timeout: 300
```

### ML Configuration
```yaml
ml:
  enabled: true
  model_path: "models/"
  training_frequency: 3600  # seconds
  prediction_horizon: 3600  # seconds
  feature_window: 100
  algorithms:
    usage_prediction: "RandomForest"
    performance_optimization: "LinearRegression"
    anomaly_detection: "IsolationForest"
```

### Container Configuration
```yaml
containers:
  enabled: true
  orchestrator: "docker"
  auto_scaling: true
  max_containers: 10
  resource_limits:
    cpu: "2.0"
    memory: "2G"
    gpu: false
```

### Cache Configuration
```yaml
cache:
  type: "redis"
  redis_url: "redis://localhost:6379/0"
  ttl: 3600
  max_size: 1000
  compression: true
```

## Monitoring and Observability

### Key Metrics to Monitor

#### System Metrics
- **CPU Usage**: Should stay below 80%
- **Memory Usage**: Should stay below 80%
- **Disk Usage**: Should stay below 90%
- **Response Time**: Should stay below 5 seconds

#### Application Metrics
- **Active Skills**: Number of loaded skills
- **Cache Hit Rate**: Should be above 70%
- **Request Rate**: Requests per second
- **Error Rate**: Should be below 1%

#### ML Metrics
- **Prediction Accuracy**: Should be above 80%
- **Anomaly Score**: Should be below 0.5
- **Resource Utilization**: Should be optimized

### Grafana Dashboards

Access the monitoring dashboard at `http://localhost:3000` with credentials `admin/admin`.

#### Dashboard Sections
1. **System Overview**: Server status and basic metrics
2. **Performance Metrics**: CPU, memory, response times
3. **Skill Management**: Active skills, cache performance
4. **ML Insights**: Prediction accuracy, anomaly detection
5. **Container Orchestration**: Auto-scaling status

### Prometheus Alerts

Configure alerts in `monitoring/prometheus.yml`:

```yaml
groups:
- name: mcp_server_alerts
  rules:
  - alert: HighCPUUsage
    expr: mcp_system_cpu_usage > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High CPU usage detected"
      
  - alert: HighMemoryUsage
    expr: mcp_system_memory_usage > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High memory usage detected"
```

## Troubleshooting

### Common Issues

#### 1. Redis Connection Issues
```bash
# Check Redis status
redis-cli ping

# Check connection from application
python -c "import redis; r = redis.from_url('redis://localhost:6379/0'); print(r.ping())"
```

#### 2. Docker Container Issues
```bash
# Check container logs
docker logs mcp-server-v3

# Check container status
docker ps

# Restart containers
docker-compose -f docker-compose.v3.yml restart
```

#### 3. ML Model Issues
```bash
# Check model files
ls models/

# Rebuild models
python -c "from enhanced_mcp_server_v3 import MLModelManager; ml = MLModelManager(config); ml._initialize_models()"
```

#### 4. Performance Issues
```bash
# Check system resources
htop

# Check application metrics
curl http://localhost:8000/metrics

# Check slow queries
docker logs mcp-server-v3 | grep "slow"
```

### Debug Mode

Enable debug mode for detailed logging:

```yaml
server:
  debug: true
monitoring:
  log_level: "DEBUG"
```

### Log Analysis

```bash
# View application logs
tail -f enhanced_mcp_server_v3.log

# View Docker logs
docker-compose -f docker-compose.v3.yml logs -f

# Search for errors
grep -i error enhanced_mcp_server_v3.log
```

## Performance Optimization

### 1. Resource Tuning
```yaml
# Adjust worker count based on CPU cores
server:
  workers: 4  # Should match CPU cores

# Optimize cache settings
cache:
  max_size: 2000
  ttl: 7200  # 2 hours
```

### 2. ML Model Optimization
```yaml
# Adjust training frequency
ml:
  training_frequency: 1800  # 30 minutes

# Optimize prediction horizon
prediction_horizon: 1800  # 30 minutes
```

### 3. Container Optimization
```yaml
# Set appropriate resource limits
containers:
  resource_limits:
    cpu: "4.0"
    memory: "4G"
```

### 4. Database Optimization
```yaml
# Optimize Redis settings
cache:
  redis_url: "redis://localhost:6379/0?max_connections=100"
```

## Security Considerations

### 1. Network Security
- Use HTTPS with valid SSL certificates
- Configure firewall rules
- Use VPN for production access

### 2. Authentication
```yaml
security:
  api_key_required: true
  jwt_secret: "your-secret-key"
  rate_limit: 1000
```

### 3. Container Security
- Use minimal base images
- Run containers as non-root user
- Regularly update base images
- Scan for vulnerabilities

### 4. Data Protection
- Encrypt sensitive configuration
- Use secure Redis passwords
- Regularly backup data
- Implement data retention policies

## Scaling Strategies

### Horizontal Scaling
```bash
# Scale containers
docker-compose -f docker-compose.v3.yml up --scale mcp-server-v3=3

# Use Kubernetes for auto-scaling
kubectl scale deployment mcp-server-v3 --replicas=5
```

### Vertical Scaling
- Increase CPU and memory limits
- Use faster storage (SSD)
- Optimize network configuration

### Load Balancing
- Use Nginx for request distribution
- Configure health checks
- Implement circuit breakers

## Maintenance

### Regular Tasks
1. **Monitor logs** daily for errors
2. **Check metrics** for performance issues
3. **Update dependencies** regularly
4. **Backup configurations** and data
5. **Review security** settings

### Updates and Upgrades
```bash
# Update Docker images
docker-compose -f docker-compose.v3.yml pull
docker-compose -f docker-compose.v3.yml up -d

# Update Python dependencies
pip install --upgrade -r requirements_v3.txt

# Update ML models
python -c "from enhanced_mcp_server_v3 import MLModelManager; ml = MLModelManager(config); ml.train_models()"
```

### Backup and Recovery
```bash
# Backup configurations
tar -czf backup-config.tar.gz mcp_config.yaml docker-compose.v3.yml

# Backup models
tar -czf backup-models.tar.gz models/

# Backup logs
tar -czf backup-logs.tar.gz logs/

# Restore from backup
tar -xzf backup-config.tar.gz
tar -xzf backup-models.tar.gz
tar -xzf backup-logs.tar.gz
```

## Support and Community

### Documentation
- [API Documentation](http://localhost:8000/docs)
- [Configuration Guide](./CONFIGURATION.md)
- [Troubleshooting Guide](./TROUBLESHOOTING.md)

### Getting Help
- Check the logs for error messages
- Review the monitoring dashboards
- Search existing issues
- Create a new issue with detailed information

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## Conclusion

This deployment guide provides comprehensive instructions for setting up, configuring, and maintaining the Enhanced MCP Server v3. For additional support, refer to the documentation and community resources.

Remember to:
- Monitor your deployment regularly
- Keep dependencies updated
- Follow security best practices
- Scale based on actual usage patterns
- Backup critical data and configurations

Happy deploying! 🚀