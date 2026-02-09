"""
Configuration management for Personal Jarvis
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # CORS settings
    cors_origins: list = ["*"]
    
    # Memory settings
    vector_db_path: str = "./chroma_db"
    
    # Command execution
    command_timeout: int = 30
    safe_mode_default: bool = True
    
    # LLM settings
    default_llm_provider: str = "gpt-4"
    default_temperature: float = 0.7
    default_max_tokens: int = 2000
    
    # Speech recognition
    default_language: str = "en"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
