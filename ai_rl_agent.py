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
    


