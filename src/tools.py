import logging
from typing import Any, Optional, List, Dict

from mcp.server import FastMCP

from database import search_service
from metrics import track_tool_usage

logger = logging.getLogger(__name__)

def register_tools(mcp: FastMCP) -> None:
    """Register all MCP tools"""
    
    @mcp.tool()
    @track_tool_usage("search_certified_software")
    async def search_certified_software(query: str, start: int = 0, rows: int = 10) -> str:
        """
        Search for certified software and applications in the Red Hat ecosystem.
        
        Args:
            query: Search query string
            start: Starting index for results (default: 0)
            rows: Maximum number of results to return (default: 10, max: 50)
            
        Returns:
            Formatted string with search results
        """
        logger.info(f"Searching certified software for: {query}")
        
        try:
            params = {
                "q": query,
                "start": start,
                "rows": min(rows, 50),
                "fq": [
                    "documentKind:CertifiedSoftware OR (documentKind:EcoSolution)",
                    "(*:* -type:\"traditional application\") OR (type:\"traditional application\" AND certification_level:\"Vendor validated\")",
                    "-type:\"Vulnerability Scanner\""
                ]
            }
            
            response = await search_service.search_request(params)
            return search_service.format_search_results(response, "certified software items")
            
        except Exception as e:
            logger.error(f"Error searching certified software: {e}")
            return f"Error searching certified software: {str(e)}"

    @mcp.tool()
    @track_tool_usage("search_container_repositories")
    async def search_container_repositories(query: str, start: int = 0, rows: int = 10) -> str:
        """
        Search for container repositories and product listings.
        
        Args:
            query: Search query string
            start: Starting index for results (default: 0)
            rows: Maximum number of results to return (default: 10, max: 50)
            
        Returns:
            Formatted string with search results including container-specific information
        """
        logger.info(f"Searching container repositories for: {query}")
        
        try:
            params = {
                "q": query,
                "start": start,
                "rows": min(rows, 50),
                "fq": [
                    "documentKind:ContainerRepository AND NOT release_categories:Deprecated",
                    "documentKind:ContainerProductListing"
                ]
            }
            
            response = await search_service.search_request(params)
            result = search_service.format_search_results(response, "container repositories")
            
            # Add container-specific info
            docs = response.get("response", {}).get("docs", [])
            additional_info = []
            for i, doc in enumerate(docs, 1):
                info = []
                if doc.get('repository'):
                    info.append(f"   Repository: {doc.get('repository')}")
                if doc.get('repository_tags'):
                    tags = doc['repository_tags']
                    if isinstance(tags, list):
                        info.append(f"   Tags: {', '.join(tags[:5])}")
                if doc.get('architecture'):
                    info.append(f"   Architecture: {doc.get('architecture')}")
                if doc.get('push_date'):
                    info.append(f"   Last Push: {doc.get('push_date')}")
                if info:
                    additional_info.extend(info)
            
            if additional_info:
                result += "\n" + "\n".join(additional_info)
            
            return result
            
        except Exception as e:
            logger.error(f"Error searching container repositories: {e}")
            return f"Error searching container repositories: {str(e)}"

    @mcp.tool()
    @track_tool_usage("search_business_partners")
    async def search_business_partners(query: str, start: int = 0, rows: int = 10) -> str:
        """
        Search for Red Hat business partners and consulting firms.
        
        Args:
            query: Search query string
            start: Starting index for results (default: 0)
            rows: Maximum number of results to return (default: 10, max: 50)
            
        Returns:
            Formatted string with search results including partner-specific information
        """
        logger.info(f"Searching business partners for: {query}")
        
        try:
            params = {
                "q": query,
                "start": start,
                "rows": min(rows, 50),
                "fq": "documentKind:BusinessPartner"
            }
            
            response = await search_service.search_request(params)
            result = search_service.format_search_results(response, "business partners")
            
            # Add partner-specific info
            docs = response.get("response", {}).get("docs", [])
            additional_info = []
            for i, doc in enumerate(docs, 1):
                info = []
                if doc.get('industry'):
                    industries = doc['industry']
                    if isinstance(industries, list):
                        info.append(f"   Industries: {', '.join(industries[:3])}")
                    else:
                        info.append(f"   Industry: {industries}")
                if doc.get('practice_accelerator_specializations'):
                    specs = doc['practice_accelerator_specializations']
                    if isinstance(specs, list):
                        info.append(f"   Specializations: {', '.join(specs[:3])}")
                if doc.get('total_accreditations'):
                    info.append(f"   Accreditations: {doc.get('total_accreditations')}")
                if info:
                    additional_info.extend(info)
            
            if additional_info:
                result += "\n" + "\n".join(additional_info)
            
            return result
            
        except Exception as e:
            logger.error(f"Error searching business partners: {e}")
            return f"Error searching business partners: {str(e)}"

    @mcp.tool()
    @track_tool_usage("search_certified_hardware")
    async def search_certified_hardware(query: str, start: int = 0, rows: int = 10) -> str:
        """
        Search for certified hardware systems and components.
        
        Args:
            query: Search query string
            start: Starting index for results (default: 0)
            rows: Maximum number of results to return (default: 10, max: 50)
            
        Returns:
            Formatted string with search results
        """
        logger.info(f"Searching certified hardware for: {query}")
        
        try:
            params = {
                "q": query,
                "start": start,
                "rows": min(rows, 50),
                "fq": "documentKind:CertifiedHardware AND NOT certified_category:\"Cloud Instance Type\""
            }
            
            response = await search_service.search_request(params)
            return search_service.format_search_results(response, "certified hardware items")
            
        except Exception as e:
            logger.error(f"Error searching certified hardware: {e}")
            return f"Error searching certified hardware: {str(e)}"

    @mcp.tool()
    @track_tool_usage("search_cloud_solutions")
    async def search_cloud_solutions(query: str, start: int = 0, rows: int = 10) -> str:
        """
        Search for cloud solutions and cloud provider partnerships.
        
        Args:
            query: Search query string
            start: Starting index for results (default: 0)
            rows: Maximum number of results to return (default: 10, max: 50)
            
        Returns:
            Formatted string with search results
        """
        logger.info(f"Searching cloud solutions for: {query}")
        
        try:
            params = {
                "q": query,
                "start": start,
                "rows": min(rows, 50),
                "fq": "certified_category:(\"Cloud Instance Type\" OR \"Cloud Image\") AND NOT certified_category:\"Cloud Instance\""
            }
            
            response = await search_service.search_request(params)
            return search_service.format_search_results(response, "cloud solutions")
            
        except Exception as e:
            logger.error(f"Error searching cloud solutions: {e}")
            return f"Error searching cloud solutions: {str(e)}"

    @mcp.tool()
    @track_tool_usage("general_catalog_search")
    async def general_catalog_search(query: str, start: int = 0, rows: int = 10, document_kinds: Optional[List[str]] = None) -> str:
        """
        General search across all Red Hat catalog types with faceting.
        
        Args:
            query: Search query string
            start: Starting index for results (default: 0)
            rows: Maximum number of results to return (default: 10, max: 50)
            document_kinds: Optional list of document kinds to filter by
            
        Returns:
            Formatted string with search results and facet information
        """
        logger.info(f"General catalog search for: {query}")
        
        try:
            # Build filter query for all main document types
            base_fq = [
                "documentKind:BusinessPartner OR documentKind:EcoSolution OR (documentKind:CertifiedSoftware) OR (documentKind:ContainerProductListing) OR (certified_category:(\"Cloud Instance Type\" OR \"Cloud Image\") AND NOT certified_category:\"Cloud Instance\") OR (documentKind:CertifiedHardware AND NOT certified_category:\"Cloud Instance Type\") OR (documentKind:ContainerRepository AND NOT release_categories:Deprecated)",
                "(*:* -type:\"traditional application\") OR (type:\"traditional application\" AND certification_level:\"Vendor validated\")",
                "-type:\"Vulnerability Scanner\""
            ]
            
            # Add document kind filter if specified
            if document_kinds:
                kind_filter = " OR ".join([f"documentKind:{kind}" for kind in document_kinds])
                base_fq.append(f"({kind_filter})")
            
            params = {
                "q": query,
                "start": start,
                "rows": min(rows, 50),
                "fq": base_fq
            }
            
            response = await search_service.search_request(params)
            result = search_service.format_search_results(response, "catalog items")
            
            # Add facet information
            facet_counts = response.get("facet_counts", {})
            facet_fields = facet_counts.get("facet_fields", {})
            
            if facet_fields:
                facet_info = ["\n📊 Search Facets:"]
                
                # Document kinds
                if "documentKind" in facet_fields:
                    doc_kinds = facet_fields["documentKind"]
                    if doc_kinds:
                        facet_info.append("   Document Types:")
                        for i in range(0, min(len(doc_kinds), 10), 2):
                            if i + 1 < len(doc_kinds):
                                facet_info.append(f"     - {doc_kinds[i]}: {doc_kinds[i + 1]}")
                
                # Partner names
                if "partnerName" in facet_fields:
                    partners = facet_fields["partnerName"]
                    if partners:
                        facet_info.append("   Top Partners:")
                        for i in range(0, min(len(partners), 6), 2):
                            if i + 1 < len(partners):
                                facet_info.append(f"     - {partners[i]}: {partners[i + 1]}")
                
                result += "\n" + "\n".join(facet_info)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in general catalog search: {e}")
            return f"Error in general catalog search: {str(e)}" 