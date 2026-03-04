FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (security team might need specific tools)
RUN apt-get update && apt-get install -y \
    git \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code from restructured src directory
COPY src/ /app/src/
# skill_registry and domains will be mounted as volumes for live updates/compliance

# Default environment variables
ENV PORT=8000
ENV MCP_TRANSPORT=http
ENV PYTHONPATH=/app
ENV REGISTRY_FILE=/app/skill_registry.json
ENV SKILLS_DIR=/app/domains
ENV TELEMETRY_LOG=/app/telemetry/usage_log.jsonl

# Expose the configured port
EXPOSE 8000

# Healthcheck to ensure MCP server is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/ || exit 1

# Start the shared server core
CMD ["python", "src/core/mcp_server.py"]
