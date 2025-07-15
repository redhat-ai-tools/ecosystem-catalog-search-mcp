FROM registry.fedoraproject.org/fedora:40

# Install system dependencies
RUN dnf install -y python3 python3-pip git \
    && dnf clean all

# Install UV
RUN pip3 install uv

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies using UV
RUN uv sync

# Create cache directory and set proper permissions for OpenShift random UIDs
RUN mkdir -p /app/.cache && chmod -R 777 /app/.cache

# Create a non-root user but make directories writable for any UID (OpenShift requirement)
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    chmod -R g+rwX /app && \
    chgrp -R 0 /app

USER appuser

# Set environment variables
ENV MCP_TRANSPORT=stdio
ENV ENABLE_METRICS=false
ENV METRICS_PORT=8000
ENV UV_CACHE_DIR=/app/.cache

# Expose metrics port
EXPOSE 8000

# Run the server
CMD ["uv", "run", "python", "src/mcp_server.py"] 