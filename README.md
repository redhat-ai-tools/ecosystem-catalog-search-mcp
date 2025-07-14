# Red Hat Search MCP Server

A Model Context Protocol (MCP) server that provides access to Red Hat's ecosystem catalog using the REST search API. This server enables AI assistants to search for certified software, container repositories, business partners, hardware, and cloud solutions through a standardized interface.

## Overview

This MCP server connects to Red Hat's ecosystem catalog search API and provides six main tools for searching different types of Red Hat ecosystem content:

- **`search_certified_software`** - Search for certified software and applications
- **`search_container_repositories`** - Search for container repositories and product listings  
- **`search_business_partners`** - Search for Red Hat business partners and consulting firms
- **`search_certified_hardware`** - Search for certified hardware systems and components
- **`search_cloud_solutions`** - Search for cloud solutions and cloud provider partnerships
- **`general_catalog_search`** - General search across all catalog types with faceting

## Features

### Data Sources
The server connects to Red Hat's ecosystem catalog search API at:
- `https://access.redhat.com/hydra/rest/search/kcs`

### Available Tools

#### 1. Search Certified Software (`search_certified_software`)
Search for certified software and applications in the Red Hat ecosystem:
- Filters for certified software and ecosystem solutions
- Excludes traditional applications unless vendor validated
- Excludes vulnerability scanners
- Returns software titles, descriptions, platforms, and certification details

#### 2. Search Container Repositories (`search_container_repositories`)
Search for container repositories and product listings:
- Filters for container repositories and product listings
- Excludes deprecated releases
- Returns repository information, tags, architecture, and push dates
- Includes container-specific metadata

#### 3. Search Business Partners (`search_business_partners`)
Search for Red Hat business partners and consulting firms:
- Filters for business partner documents
- Returns partner information, industries, specializations, and accreditations
- Includes partner-specific metadata like practice accelerator specializations

#### 4. Search Certified Hardware (`search_certified_hardware`)
Search for certified hardware systems and components:
- Filters for certified hardware documents
- Excludes cloud instance types (handled separately)
- Returns hardware titles, descriptions, platforms, and certification details

#### 5. Search Cloud Solutions (`search_cloud_solutions`)
Search for cloud solutions and cloud provider partnerships:
- Filters for cloud instance types and cloud images
- Returns cloud solution information and provider partnerships
- Includes cloud-specific metadata

#### 6. General Catalog Search (`general_catalog_search`)
General search across all Red Hat catalog types with faceting:
- Searches across all document types
- Provides faceted search results with counts by document type and partner
- Optional filtering by specific document kinds
- Returns comprehensive search results with metadata

### Search Parameters

All search tools support the following parameters:
- **`query`** - Search query string (required)
- **`start`** - Starting index for results (default: 0)
- **`rows`** - Maximum number of results to return (default: 10, max: 50)

The `general_catalog_search` tool additionally supports:
- **`document_kinds`** - Optional list of document kinds to filter by

### Monitoring & Metrics

The server includes optional Prometheus metrics support for monitoring:
- **Tool usage tracking** - Track calls to each MCP tool with success/error rates and duration
- **Search API monitoring** - Monitor Red Hat API request performance and success rates
- **Connection tracking** - Track active MCP connections
- **HTTP endpoints** - `/metrics` for Prometheus scraping and `/health` for health checks

## Prerequisites

- Python 3.10+
- [UV](https://docs.astral.sh/uv/) (Python package manager)
- Podman or Docker (for containerized deployment)
- Internet access to reach Red Hat's search API

## Architecture

The codebase is organized into modular components in the `src/` directory:

- **`src/mcp_server.py`** - Main server entry point and MCP initialization
- **`src/config.py`** - Configuration management and environment variable handling  
- **`src/database.py`** - HTTP client handling for Red Hat search API requests
- **`src/tools.py`** - MCP tool implementations and business logic
- **`src/metrics.py`** - Optional Prometheus metrics collection and HTTP server

## Environment Variables

The following environment variables are used to configure the server:

### Optional
- **`MCP_TRANSPORT`** - Transport protocol for MCP communication  
  - Default: `sse`
- **`ENABLE_METRICS`** - Enable Prometheus metrics collection  
  - Default: `false`
- **`METRICS_PORT`** - Port for metrics HTTP server  
  - Default: `8000`

## Installation & Setup

### Using UV (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd ecosystem-catalog-search-mcp
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv sync
```

4. Run the server:
```bash
uv run python src/mcp_server.py
```

### Using pip

1. Clone the repository:
```bash
git clone <repository-url>
cd ecosystem-catalog-search-mcp
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python src/mcp_server.py
```

## Development

### Transport Options

The server supports multiple transport methods:

#### Standard I/O (stdio)
Default transport for CLI usage:
```bash
python src/mcp_server.py --transport stdio
```

#### Server-Sent Events (SSE)
For web browser compatibility:
```bash
python src/mcp_server.py --transport sse
```

### Metrics and Monitoring

Enable Prometheus metrics:
```bash
ENABLE_METRICS=true METRICS_PORT=8000 python src/mcp_server.py
```

Access metrics:
- Metrics: `http://localhost:8000/metrics`
- Health check: `http://localhost:8000/health`

### Container Deployment

Build and run with Podman:
```bash
podman build -t redhat-search-mcp .
podman run -p 8000:8000 -e ENABLE_METRICS=true redhat-search-mcp
```

## Usage Examples

### Search for certified software:
```python
# Search for Ansible certified software
result = await search_certified_software("Ansible", rows=20)
```

### Search for container repositories:
```python
# Search for RHEL containers
result = await search_container_repositories("RHEL", rows=15)
```

### Search for business partners:
```python
# Search for consulting partners
result = await search_business_partners("consulting", rows=10)
```

### General catalog search:
```python
# Search across all catalog types
result = await general_catalog_search("OpenShift", rows=25)
```

## API Reference

### Search Result Format

All search tools return formatted strings with the following structure:

```
Found X <result_type>

1. <Title>
   Type: <Document Kind>
   Partner: <Partner Name>
   Category: <Category>
   Description: <Description>
   Platforms: <Supported Platforms>
   Categories: <Certification Categories>
   Last Modified: <Date>
   URL: <View URL>
```

### Faceted Search Results

The `general_catalog_search` tool includes additional facet information:

```
📊 Search Facets:
   Document Types:
     - BusinessPartner: 15
     - CertifiedSoftware: 42
   Top Partners:
     - Red Hat: 25
     - IBM: 18
```

## Error Handling

The server includes comprehensive error handling:
- Network errors are caught and logged
- Invalid search parameters are handled gracefully
- All tools return error messages instead of exceptions
- Metrics track success/failure rates

## Security

- Uses proper SSL/TLS certificate verification
- No authentication required (public API)
- Input sanitization for search queries
- Rate limiting through HTTP client configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
