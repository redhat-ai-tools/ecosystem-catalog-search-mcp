import ssl
import time
import logging
from typing import Any, Dict, Optional, List
from urllib.parse import urlencode

import httpx
import certifi

from config import SEARCH_ENDPOINT
from metrics import track_search_request

logger = logging.getLogger(__name__)

class RedHatSearchService:
    """Service for Red Hat ecosystem search"""
    
    def __init__(self):
        self.client = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create httpx client with proper SSL configuration"""
        if self.client is None:
            # Create SSL context with proper certificate verification
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            
            # Create client with SSL context
            self.client = httpx.AsyncClient(
                verify=ssl_context,
                timeout=30.0,
                limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
            )
        return self.client
    
    async def search_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a search request to the Red Hat API"""
        client = await self._get_client()
        
        start_time = time.time()
        success = False
        
        try:
            # Base parameters for all requests
            base_params = {
                "redhat_client": "ecosystem-catalog",
                "enableElevation": "false",
                "wt": "json",
                "altQueryFields": "true",
                "omitHeader": "false",
                "sort": "score desc",
                "facet": "true",
                "facet.limit": "-1",
                "facet.mincount": "1",
                "fl": "id,documentKind,allTitle,view_uri,logo_uri,partnerName,short_description,type,target_platforms,certified_RedHat_Platforms,certified_category,lastModifiedDate,partners,repository,display_data_short_description,push_date,total_accreditations,partnerProductNamespace,partnerProductName,architecture,catalog_url_id,practice_accelerator_specializations,subcategories,repository_tags,industry,freshness_grades_json,secondary_partners,practice_accelerator_specializations_count,certification_developer_count,certification_delivery_count,certification_support_engineer_count,credential_seller_count,credential_tech_seller_count",
                "f.target_platforms.facet.method": "enum",
                "facet.field": [
                    "{!ex=documentKind_tag}documentKind",
                    "{!ex=partnerName_tag}partnerName", 
                    "{!ex=platform_tag}target_platforms",
                    "{!ex=industry_tag}industry",
                    "{!ex=subcategories_tag}subcategories"
                ]
            }
            
            # Merge with provided parameters
            final_params = {**base_params, **params}
            
            # Handle facet.field as list
            if "facet.field" in final_params and isinstance(final_params["facet.field"], list):
                # Convert to multiple parameters for URL encoding
                facet_fields = final_params.pop("facet.field")
                query_string = urlencode(final_params, doseq=True)
                for field in facet_fields:
                    query_string += f"&facet.field={field}"
                url = f"{SEARCH_ENDPOINT}?{query_string}"
            else:
                url = f"{SEARCH_ENDPOINT}?{urlencode(final_params, doseq=True)}"
            
            response = await client.get(url)
            response.raise_for_status()
            
            success = True
            return response.json()
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during search request: {e}")
            raise Exception(f"Search request failed with status {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Request error during search: {e}")
            raise Exception(f"Search request failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            raise
        finally:
            # Track metrics
            track_search_request(start_time, success)
    
    def format_search_results(self, response: Dict[str, Any], result_type: str) -> str:
        """Format search results as text"""
        response_data = response.get("response", {})
        docs = response_data.get("docs", [])
        num_found = response_data.get("numFound", 0)
        
        output = [f"Found {num_found} {result_type}"]
        
        if not docs:
            output.append("No results found")
            return "\n".join(output)
        
        for i, doc in enumerate(docs, 1):
            output.append(f"\n{i}. {doc.get('allTitle', 'No Title')}")
            output.append(f"   Type: {doc.get('documentKind', 'N/A')}")
            
            if doc.get('partnerName'):
                output.append(f"   Partner: {doc.get('partnerName')}")
            
            if doc.get('type'):
                output.append(f"   Category: {doc.get('type')}")
            
            if doc.get('short_description'):
                desc = doc['short_description'][:150] + "..." if len(doc['short_description']) > 150 else doc['short_description']
                output.append(f"   Description: {desc}")
            
            if doc.get('target_platforms'):
                platforms = doc['target_platforms']
                if isinstance(platforms, list):
                    output.append(f"   Platforms: {', '.join(platforms[:3])}")
                else:
                    output.append(f"   Platforms: {platforms}")
            
            if doc.get('certified_category'):
                categories = doc['certified_category']
                if isinstance(categories, list):
                    output.append(f"   Categories: {', '.join(categories[:2])}")
                else:
                    output.append(f"   Categories: {categories}")
            
            if doc.get('lastModifiedDate'):
                output.append(f"   Last Modified: {doc.get('lastModifiedDate')}")
            
            if doc.get('view_uri'):
                output.append(f"   URL: {doc.get('view_uri')}")
        
        return "\n".join(output)
    
    async def cleanup(self):
        """Clean up resources"""
        if self.client:
            await self.client.aclose()
            self.client = None

# Global search service instance
search_service = RedHatSearchService() 