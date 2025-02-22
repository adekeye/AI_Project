from pydantic import BaseModel, Field
from typing import Dict, List
from agno.agent import agent
from streamlit import streamlit
from firecrawl import FirecrawlApp
from agno.models.openai import OpenAIcht


class AssetDetails(BaseModel):
    "data model for real estate asset information extraction"

    asset_name: str = Field(description="Official name of the asset", alias="Asset_Name")
    category: str = Field (
        description="Category of property (e.g., commercial, residential)", alias="Property_Category"
    )
    address: str = Field (description="Full address of asset")
    market_value: str = Field(
        description="Market value of the property", alias="Market_Value"
    )
    details: str = Field(
        description="Comprehensive details about the asset", alias="Asset_Description"
    )


class AssetsResponse(BaseModel):
    """Data model for multiple asset responses."""
    assets: List[AssetDetails] = Field(
        description="List of detailed real estate asset information"
    )

class AreaMetrics(BaseModel):
    """Data model for regional price trends and performance."""
    region: str
    cost_per_sqft: float
    growth_rate: float
    rental_return: float

class Arearesponse(BaseModel):
    """Data model for multiple Area Response"""
    areas: List[AreaMetrics] = Field(description="List of area data points")

class FirecrawlResponse(BaseModel):
    """Data model for firecrawl API response"""
    success: bool
    data: Dict
    status: str
    expiresAt: str

class AssetSearchAdvisor:
    """Agent responsible for locating assets and offering recommendations."""

    def __init__(self, firecrawl_api_key: str, openai_api_key: str, model_id: str = "o3-mini"):
        self.agent = Agent(
            model=OpenAIcht(id=model_id, api_key=openai_api_key),
            markdown=True,
            details="I am an asset specialist with expertise in sourcing and evaluating properties tailored to individual client preferences."
        )
        self.firecrawl = FirecrawlApp(api_key=firecrawl_api_key)
        

        def search_assets(
            self, 
            city: str,
            price_cap: float,
            asset_category: str = "Residential",
            asset_type: str = "Flat"
        ) -> str:
            """Locate and evaluate assets according to client criteria."""
            formatted_city = city.lower()
    
            urls = [
                f"https://www.zillow.com/{formatted_city}"
                f"https://www.trulia.com/home/{formatted_city}"
                f"https://www.redfin.com/{formatted_city}"
                f"https://www.realtor.com/{formatted_city}"
        
                    ]
            asset_prompt = "Apartments" if asset_type == "Flat" else "Standalone Homes"

            raw_response = self.firecrawl.extract(
                urls = urls,
                params = {
                    'prompt': f"""Extract ONLY 10 OR LESS different {asset_category} {asset_prompt} from {city} that cost less than {price_cap} crores.
                
                    Requirements:
                    - Asset Category: {asset_category} properties only
                    - Asset Type: {asset_prompt} only
                    - Location: {city}
                    - Maximum Price: {price_cap} crores
                    - Include complete asset details with exact location
                    - IMPORTANT: Return data for at least 3 different assets. MAXIMUM 10.
                    - Format as a list of assets with their respective details
                    """,
                    'schema': AssetsResponse.model_json_schema()
                    }

                )

            print("Raw Asset Response:", raw_response)









