import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.utils.ai_client import MultiModelClient

@pytest.mark.asyncio
async def test_multi_model_client_initialization():
    """Verify that clients are initialized based on available config."""
    with patch("src.utils.ai_client.config") as mock_config:
        mock_config.ANTHROPIC_API_KEY = "test_key"
        mock_config.GOOGLE_API_KEY = "test_key"
        mock_config.GROQ_API_KEY = None
        mock_config.MISTRAL_API_KEY = None
        mock_config.OPENROUTER_API_KEY = "test_key"
        mock_config.LOCAL_AI_BASE_URL = "http://localhost:8080/v1"
        mock_config.LOCAL_AI_MODEL = "llama3"
        
        # Patch the specific clients
        with patch("src.utils.ai_client.anthropic.AsyncAnthropic"), \
             patch("src.utils.ai_client.genai.Client"), \
             patch("src.utils.ai_client.AsyncOpenAI"):
            
            multi_client = MultiModelClient()
            assert "anthropic" in multi_client.clients
            assert "gemini" in multi_client.clients
            assert "groq" not in multi_client.clients
            assert "openrouter" in multi_client.clients
            assert "local" in multi_client.clients

@pytest.mark.asyncio
async def test_multi_model_query_all():
    """Verify that query_all correctly aggregates responses."""
    multi_client = MultiModelClient()
    
    # Mock each client's generate_text method
    mock_anthropic = AsyncMock(return_value="Claude Response")
    mock_local = AsyncMock(return_value="Local Response")
    
    multi_client.clients = {
        "anthropic": MagicMock(generate_text=mock_anthropic),
        "local": MagicMock(generate_text=mock_local)
    }
    
    results = await multi_client.query_all("Test Prompt")
    
    assert results["anthropic"] == "Claude Response"
    assert results["local"] == "Local Response"
    assert len(results) == 2
