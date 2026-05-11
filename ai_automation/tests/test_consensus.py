import pytest
from unittest.mock import AsyncMock, MagicMock
from src.utils.consensus import ConsensusSynthesizer

@pytest.mark.asyncio
async def test_consensus_synthesize():
    """Verify that synthesize correctly formats model inputs and calls the synthesizer."""
    mock_multi_client = MagicMock()
    mock_primary_client = AsyncMock()
    mock_primary_client.generate_text.return_value = "Final Synthesis"
    
    # Setup mock clients — must include all models that appear in responses
    mock_multi_client.clients = {
        "gemini": mock_primary_client,
        "groq": mock_primary_client,
    }
    
    synthesizer = ConsensusSynthesizer(mock_multi_client)
    
    responses = {
        "gemini": "Gemini Response",
        "groq": "Groq Response"
    }
    
    result = await synthesizer.synthesize("Write a blog post", responses)
    
    assert result == "Final Synthesis"
    # Verify that the synthesis prompt contains model names and content
    args, kwargs = mock_primary_client.generate_text.call_args
    synthesis_prompt = args[0]
    assert "Gemini Response" in synthesis_prompt
    assert "Groq Response" in synthesis_prompt
    assert "### Model: gemini" in synthesis_prompt

@pytest.mark.asyncio
async def test_run_consensus_flow():
    """Verify that the full flow (Query All -> Synthesize) works correctly."""
    mock_multi_client = MagicMock()
    mock_multi_client.query_all = AsyncMock(return_value={
        "anthropic": "Claude Output",
        "gemini": "Gemini Output",
        "error_model": "Error: Something went wrong"
    })
    
    # We also need to mock the primary model for synthesis
    mock_primary_client = AsyncMock(return_value="Synthesized Output")
    mock_multi_client.clients = {"anthropic": MagicMock(generate_text=mock_primary_client)}
    
    synthesizer = ConsensusSynthesizer(mock_multi_client)
    # Patch synthesize to verify it was called correctly
    synthesizer.synthesize = AsyncMock(return_value="Final Synthesized Result")
    
    result = await synthesizer.run_consensus_flow("Test Prompt")
    
    assert result == "Final Synthesized Result"
    # Verify that errors were filtered out before synthesis
    synthesizer.synthesize.assert_called_once()
    passed_responses = synthesizer.synthesize.call_args[0][1]
    assert "error_model" not in passed_responses
    assert "anthropic" in passed_responses
    assert "gemini" in passed_responses
