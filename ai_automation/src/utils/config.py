import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    """
    Secure configuration management for the AI-Driven SEO & Content MVP.
    Uses pydantic-settings to automatically load variables from .env.
    """
    # AI API Keys
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    MISTRAL_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    TAVILY_API_KEY: Optional[str] = None

    # Local AI Configuration
    LOCAL_AI_BASE_URL: str = "http://localhost:11434/v1"
    LOCAL_AI_MODEL: str = "minimax-m2.7:cloud"

    # Project Settings
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Security: Use .env file for local development
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Global configuration instance
config = Config()
