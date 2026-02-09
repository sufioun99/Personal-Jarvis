"""
Configuration management for JARVIS AI Assistant
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # OpenAI Configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    
    # Anthropic Claude
    anthropic_api_key: str = ""
    
    # Google AI
    google_api_key: str = ""
    google_application_credentials: Optional[str] = None
    
    # ElevenLabs for TTS
    elevenlabs_api_key: str = ""
    
    # Vector Database
    pinecone_api_key: str = ""
    pinecone_environment: str = "gcp-starter"
    
    # Redis for Message Queue
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # Search APIs
    google_search_api_key: str = ""
    google_search_engine_id: str = ""
    bing_search_api_key: str = ""
    
    # Weather API
    openweather_api_key: str = ""
    
    # News API
    news_api_key: str = ""
    
    # GitHub
    github_token: str = ""
    
    # AWS
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    
    # Application Settings
    jarvis_host: str = "0.0.0.0"
    jarvis_port: int = 8000
    jarvis_debug: bool = False
    
    # Wake Word
    wake_word: str = "hey jarvis"
    
    # Safety Settings
    enable_sudo: bool = False
    require_confirmation: bool = True
    command_whitelist: str = "ls,cd,pwd,cat,grep,find,ps,df,free,top,htop"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "jarvis.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def whitelisted_commands(self) -> List[str]:
        """Parse command whitelist into a list"""
        return [cmd.strip() for cmd in self.command_whitelist.split(",")]


# Global settings instance
settings = Settings()
