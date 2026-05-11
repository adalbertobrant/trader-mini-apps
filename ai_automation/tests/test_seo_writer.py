import pytest
from unittest.mock import AsyncMock, MagicMock
from src.content.seo_writer import SEOWriter

@pytest.mark.asyncio
async def test_seo_writer_write_article():
    """Verify that SEOWriter utilizes research context and consensus flow."""
    mock_synthesizer = AsyncMock()
    mock_synthesizer.run_consensus_flow.return_value = "Full SEO Optimized Article"
    
    writer = SEOWriter(mock_synthesizer)
    
    topic = "The Future of AI Automation"
    research_context = "Audience: Tech Savvy. Competitors: High. Key Pain: Manual data entry."
    
    result = await writer.write_article(topic, research_context)
    
    assert result == "Full SEO Optimized Article"
    
    # Verify the prompt passed to the synthesizer contains the context
    args, kwargs = mock_synthesizer.run_consensus_flow.call_args
    prompt = args[0]
    assert topic in prompt
    assert "Manual data entry" in prompt
    assert "SEO Title" in prompt

@pytest.mark.asyncio
async def test_seo_writer_generate_meta():
    """Verify SEO meta data generation."""
    mock_synthesizer = AsyncMock()
    mock_synthesizer.run_consensus_flow.return_value = "SEO Title & Meta"
    
    writer = SEOWriter(mock_synthesizer)
    
    result = await writer.generate_seo_meta("Long article content...")
    
    assert result == "SEO Title & Meta"
    args, kwargs = mock_synthesizer.run_consensus_flow.call_args
    prompt = args[0]
    assert "Long article content" in prompt
