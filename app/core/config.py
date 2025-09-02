from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Database
    database_url: str = "sqlite:///./taxi24.db"
    
    # API
    api_title: str = "Taxi24 API"
    api_description: str = "REST API for Taxi24 - A taxi service management system"
    api_version: str = "1.0.0"
    
    # Business Logic
    default_search_radius_km: float = 3.0
    tax_rate: float = 0.18  # 18% tax
    max_nearby_drivers: int = 3
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"


settings = Settings()