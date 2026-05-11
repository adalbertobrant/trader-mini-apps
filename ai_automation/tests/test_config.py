import os
import pytest
from src.utils.config import Config

def test_config_loading_from_env(monkeypatch):
    """Verify that Config loads values from environment variables."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test_anthropic_key")
    monkeypatch.setenv("TAVILY_API_KEY", "test_tavily_key")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_openrouter_key")
    monkeypatch.setenv("DEBUG", "True")
    
    test_config = Config()
    
    assert test_config.ANTHROPIC_API_KEY == "test_anthropic_key"
    assert test_config.TAVILY_API_KEY == "test_tavily_key"
    assert test_config.OPENROUTER_API_KEY == "test_openrouter_key"
    assert test_config.DEBUG is True

def test_config_default_values():
    """Verify default values are correctly set."""
    test_config = Config()
    assert test_config.LOCAL_AI_BASE_URL == "http://localhost:11434/v1"
    assert test_config.LOCAL_AI_MODEL == "minimax-m2.7:cloud"
