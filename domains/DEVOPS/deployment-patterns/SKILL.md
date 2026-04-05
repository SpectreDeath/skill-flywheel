---
name: deployment-patterns
description: "Use when: setting up deployment infrastructure, planning releases, configuring CI/CD pipelines, implementing Docker containerization, setting up health checks, or planning rollback strategies. Triggers: 'deploy', 'deployment', 'CI/CD', 'pipeline', 'Docker', 'containerize', 'release', 'rollback', 'health check', 'production ready'. NOT for: local development only, or when deployment is handled by external services without customization."
---

# Deployment Patterns

Deployment workflows, CI/CD pipeline patterns, Docker containerization, health checks, rollback strategies, and production readiness checklists for web applications.

## When to Use This Skill

Use this skill when:
- Setting up deployment infrastructure
- Planning releases and deployments
- Configuring CI/CD pipelines
- Implementing Docker containerization
- Setting up health checks
- Planning rollback strategies
- Creating production readiness checklists
- Debugging deployment issues

Do NOT use when:
- Local development only
- Deployment handled entirely by external services
- Simple static site deployments
- Proof of concept that won't go to production

## CI/CD Pipeline Patterns

### Basic Pipeline Structure
```yaml
stages:
  - lint
  - test
  - build
  - deploy

lint:
  script: npm run lint
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    
test:
  script: npm run test:ci
  coverage: /Coverage: \d+\.\d+/
  
build:
  script: 
    - npm run build
    - docker build -t $IMAGE_TAG .
  artifacts:
    paths:
      - dist/
      - Dockerfile
      
deploy:
  script: ./deploy.sh
  environment:
    name: production
  only:
    - main
```

### Multi-Environment Promotion
```yaml
stages:
  - build
  - test
  - staging
  - production

deploy-staging:
  stage: staging
  script: ./deploy.sh staging
  environment:
    name: staging
  only:
    - main
    
deploy-production:
  stage: production
  script: ./deploy.sh production
  environment:
    name: production
  when: manual
  allow_failure: false
```

### Progressive Delivery
- **Canary Deployments**: Route small percentage of traffic to new version
- **Blue-Green Deployments**: Switch between identical environments
- **Rolling Deployments**: Gradually replace instances
- **Feature Flags**: Toggle features independent of deployment

## Docker Containerization

### Multi-stage Build Pattern
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### Security Best Practices
```dockerfile
# Use specific version, not latest
FROM node:20.11.0-alpine3.19

# Run as non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# Read-only filesystem where possible
COPY --chown=nodejs:nodejs . .
```

## Health Checks

### Types of Health Checks

#### 1. Liveness Probe
Confirms container is running (not stuck in crash loop)
```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3
```

#### 2. Readiness Probe
Confirms container can handle requests (not overloaded)
```yaml
readinessProbe:
  httpGet:
    path: /health/ready
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 3
```

#### 3. Startup Probe
For slow-starting applications
```yaml
startupProbe:
  httpGet:
    path: /health/startup
    port: 3000
  failureThreshold: 30
  periodSeconds: 10
```

### Health Endpoint Implementation
```javascript
app.get('/health/live', (req, res) => {
  res.json({ status: 'alive' });
});

app.get('/health/ready', async (req, res) => {
  const checks = await Promise.all([
    checkDatabase(),
    checkCache(),
    checkExternalServices()
  ]);
  
  const ready = checks.every(c => c.healthy);
  res.status(ready ? 200 : 503).json({
    status: ready ? 'ready' : 'not ready',
    checks
  });
});
```

## Rollback Strategies

### Automated Rollback Triggers
```yaml
deploy:
  script: ./deploy.sh
  rollback:
    on_failure:
      - kubectl rollout undo deployment/app
    on_metric:
      - metric: error_rate
        threshold: 5%
        action: rollback
      - metric: latency_p99
        threshold: 1000ms
        action: rollback
```

### Manual Rollback Process
```bash
# View deployment history
kubectl rollout history deployment/app

# Rollback to previous revision
kubectl rollout undo deployment/app

# Rollback to specific revision
kubectl rollout undo deployment/app --to-revision=3
```

## Production Readiness Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Code review completed
- [ ] Security scan passed
- [ ] Performance benchmarks meet SLA
- [ ] Database migrations tested
- [ ] Feature flags configured for rollback

### Infrastructure
- [ ] Scaling policies defined
- [ ] Monitoring alerts configured
- [ ] Log aggregation working
- [ ] Health checks implemented
- [ ] Backup strategy in place
- [ ] DNS configured

### Operational
- [ ] Runbook updated
- [ ] On-call team notified
- [ ] Rollback procedure tested
- [ ] Communication plan ready
- [ ] Post-deployment monitoring active

## Deployment Patterns Comparison

| Pattern | Zero Downtime | Rollback Speed | Infrastructure Cost | Complexity |
|---------|---------------|----------------|---------------------|------------|
| Blue-Gold | Yes | Instant | 2x | Low |
| Canary | Yes | Gradual | 1x | Medium |
| Rolling | Yes | Gradual | 1x | Low |
| Recreate | No | Instant | 1x | Low |

## Constraints

- Always have rollback plan before deployment
- Health checks should be lightweight
- Blue-green requires identical infrastructure
- Canary requires traffic management capability
- Database migrations should be backwards compatible
- Feature flags should default to off for new features
