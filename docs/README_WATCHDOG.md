# Self-Healing Watchdog for MCP Infrastructure

A comprehensive monitoring and recovery system for the MCP (Model Context Protocol) infrastructure that automatically detects service failures and triggers self-healing recovery processes.

## Overview

The Self-Healing Watchdog monitors all 11 MCP services running on ports 8000-8012, checking their health every 5 minutes. When a service failure is detected, it automatically triggers the `master_flywheel()` recovery function to re-provision the entire infrastructure.

## Features

- **Continuous Monitoring**: Health checks every 5 minutes for all MCP services
- **Automatic Recovery**: Triggers `master_flywheel()` on service failures
- **Comprehensive Logging**: Detailed event logging to `flywheel_events.log`
- **Robust Error Handling**: Handles timeouts, connection errors, and exceptions
- **Graceful Shutdown**: Signal handling for clean shutdown
- **Easy Testing**: Built-in test suite for validation

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Health        │    │   Recovery       │    │   Event         │
│   Checker       │───▶│   Manager        │───▶│   Logger        │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   11 MCP        │    │   master_        │    │   flywheel_     │
│   Services      │    │   flywheel()     │    │   events.log    │
│   (8000-8012)   │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Services Monitored

| Service | Port | Description |
|---------|------|-------------|
| mcp-discovery | 8000 | Discovery service for MCP infrastructure |
| mcp-orchestration | 8001 | Orchestration service for skill management |
| mcp-security | 8002 | Security and validation service |
| mcp-data-ai | 8003 | Data and AI service |
| mcp-devops | 8004 | DevOps and infrastructure service |
| mcp-engineering | 8005 | Engineering and formal methods service |
| mcp-ux-mobile | 8006 | UX and mobile development service |
| mcp-advanced | 8007 | Advanced algorithms and quantum computing service |
| mcp-strategy | 8008 | Strategy and game theory service |
| mcp-agent-rd | 8009 | Agent research and development service |
| mcp-model-orchestration | 8012 | Model orchestration and management service |

## Installation

### Prerequisites

- Python 3.8+
- Docker (for MCP services)
- MCP infrastructure running

### Dependencies

Install required Python packages:

```bash
pip install requests
```

### Files Created

- `watchdog_monitor.py` - Main watchdog script
- `test_watchdog.py` - Test suite for validation
- `README_WATCHDOG.md` - This documentation file

## Usage

### Starting the Watchdog

```bash
# Start the watchdog monitor
python watchdog_monitor.py
```

The watchdog will:
- Monitor all 11 MCP services every 5 minutes
- Log events to `flywheel_events.log`
- Display status updates in real-time
- Handle service failures automatically

### Stopping the Watchdog

Press `Ctrl+C` to stop the watchdog gracefully.

### Testing the System

Run the test suite to validate functionality:

```bash
# Run all tests
python test_watchdog.py

# Or run specific tests
python test_watchdog.py --health-check    # Test health checking
python test_watchdog.py --docker-status   # Check Docker services
python test_watchdog.py --log-file        # Test log functionality
```

## Configuration

### Monitoring Intervals

Edit `watchdog_monitor.py` to adjust timing:

```python
MONITORING_INTERVAL = 300  # 5 minutes (300 seconds)
HEALTH_CHECK_TIMEOUT = 5   # 5 seconds timeout per service
RECOVERY_TIMEOUT = 600     # 10 minutes timeout for recovery
```

### Log Files

- `flywheel_events.log` - Main event log with JSON format
- `watchdog_monitor.log` - Watchdog internal logging

### Service Configuration

Services are defined in the `SERVICES` list in `watchdog_monitor.py`:

```python
SERVICES = [
    {
        "name": "mcp-discovery",
        "port": 8000,
        "health_url": "http://mcp-discovery:8000/health",
        "description": "Discovery service for MCP infrastructure"
    },
    # ... other services
]
```

## Event Logging

The watchdog logs all events to `flywheel_events.log` in JSON format:

### Service Failure Event

```json
{
  "timestamp": "2026-03-09T19:45:00.123456",
  "event_type": "SERVICE_FAILURE",
  "failed_services": [
    {
      "service": "mcp-orchestration",
      "status": "TIMEOUT",
      "error": "Request timed out after 5 seconds"
    }
  ],
  "total_failed": 1
}
```

### Recovery Attempt Event

```json
{
  "timestamp": "2026-03-09T19:45:05.654321",
  "event_type": "RECOVERY_ATTEMPT",
  "failed_services": [...],
  "recovery_result": {
    "success": true,
    "return_code": 0,
    "stdout": "...",
    "stderr": ""
  },
  "recovery_successful": true
}
```

### Recovery Success Event

```json
{
  "timestamp": "2026-03-09T19:45:30.111111",
  "event_type": "RECOVERY_SUCCESS",
  "recovered_services": ["mcp-orchestration"],
  "total_recovered": 1
}
```

## Testing the Self-Healing Functionality

### Manual Testing Steps

1. **Start the watchdog**:
   ```bash
   python watchdog_monitor.py
   ```

2. **Stop a service** (in another terminal):
   ```bash
   docker stop mcp-orchestration
   ```

3. **Observe the watchdog**:
   - Should detect failure within 5 minutes
   - Should log the failure to `flywheel_events.log`
   - Should trigger `master_flywheel()` recovery
   - Should log recovery attempt and results

4. **Verify recovery**:
   - Check that all services are restored
   - Review `flywheel_events.log` for complete event chain

### Automated Testing

Use the test script to validate components:

```bash
# Test health checking without stopping services
python test_watchdog.py

# When prompted, choose to run recovery simulation
# This will stop and restart a service to test the recovery process
```

## Troubleshooting

### Common Issues

1. **Services not responding to health checks**
   - Verify Docker services are running: `docker ps`
   - Check service logs: `docker logs mcp-orchestration`
   - Verify network connectivity between containers

2. **Recovery process fails**
   - Check `flywheel_events.log` for error details
   - Verify `discovery_service.py` is accessible
   - Check Docker compose configuration

3. **Watchdog not detecting failures**
   - Verify health endpoints are accessible
   - Check network connectivity
   - Review `watchdog_monitor.log` for errors

### Log Analysis

```bash
# View recent events
tail -f flywheel_events.log | jq .

# Search for specific event types
grep '"event_type": "SERVICE_FAILURE"' flywheel_events.log

# Check recovery success rate
grep -c '"event_type": "RECOVERY_SUCCESS"' flywheel_events.log
grep -c '"event_type": "RECOVERY_FAILURE"' flywheel_events.log
```

### Debug Mode

Enable debug logging by modifying the logging level in `watchdog_monitor.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    # ... other settings
)
```

## Integration with Existing Infrastructure

### Docker Compose Integration

Add the watchdog as a service in your `docker-compose.yml`:

```yaml
services:
  # ... existing services
  
  mcp-watchdog:
    build: .
    volumes:
      - ./watchdog_monitor.py:/app/watchdog_monitor.py
      - ./flywheel_events.log:/app/flywheel_events.log
    depends_on:
      - mcp-discovery
      - mcp-orchestration
      # ... other services
    restart: unless-stopped
```

### Systemd Service (Linux)

Create `/etc/systemd/system/mcp-watchdog.service`:

```ini
[Unit]
Description=MCP Infrastructure Watchdog
After=docker.service
Requires=docker.service

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/skill-flywheel
ExecStart=/usr/bin/python3 watchdog_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable mcp-watchdog
sudo systemctl start mcp-watchdog
```

## Security Considerations

- The watchdog runs with the same permissions as the user executing it
- Ensure proper file permissions on log files
- Consider running in a dedicated container for isolation
- Monitor the watchdog process itself for availability

## Performance Impact

- Minimal CPU usage (health checks every 5 minutes)
- Low memory footprint
- Network traffic only during health checks
- Log file growth depends on failure frequency

## Monitoring the Monitor

Consider setting up external monitoring for the watchdog itself:

- Process monitoring (ensure watchdog is running)
- Log file monitoring (detect watchdog failures)
- Alerting on repeated recovery failures

## Contributing

1. Test changes thoroughly with the test suite
2. Update documentation for new features
3. Follow Python best practices
4. Ensure backward compatibility

## License

This project is part of the Skill Flywheel system. See the main project LICENSE for details.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review log files for error details
3. Run the test suite to validate components
4. Create an issue with detailed logs and reproduction steps