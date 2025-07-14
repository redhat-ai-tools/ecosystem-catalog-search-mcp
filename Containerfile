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

# Create a non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Set environment variables
ENV MCP_TRANSPORT=stdio
ENV ENABLE_METRICS=false
ENV METRICS_PORT=8000

# Expose metrics port
EXPOSE 8000

# Run the server
CMD ["uv", "run", "python", "src/mcp_server.py"] 