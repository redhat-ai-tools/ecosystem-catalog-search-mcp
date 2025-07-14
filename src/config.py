import os
import logging

# Configure logging to stderr so it doesn't interfere with MCP protocol
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# MCP Configuration
MCP_TRANSPORT = os.environ.get("MCP_TRANSPORT", "sse")

# Red Hat Search API configuration
SEARCH_ENDPOINT = "https://access.redhat.com/hydra/rest/search/kcs"

# Prometheus metrics configuration
ENABLE_METRICS = os.environ.get("ENABLE_METRICS", "false").lower() == "true"
METRICS_PORT = int(os.environ.get("METRICS_PORT", "8000"))

# Check if Prometheus is available
try:
    from prometheus_client import Counter, Histogram, Gauge, CONTENT_TYPE_LATEST, generate_latest
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False 