import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.research.market_analyzer import MarketAnalyzer

@pytest.mark.asyncio
async def test_market_analyzer_analyze_niche():
    """Verify that MarketAnalyzer uses search context and consensus flow."""
    mock_synthesizer = AsyncMock()
    mock_synthesizer.run_consensus_flow.return_value = "Synthesized Market Report"
    
    analyzer = MarketAnalyzer(mock_synthesizer)
    
    # Mock the search client
    with patch("src.research.market_analyzer.search_client") as mock_search:
        mock_search.search_market_data = AsyncMock(return_value="Real-time Search Data")
        
        result = await analyzer.analyze_niche("AI Automation")
        
        assert result == "Synthesized Market Report"
        
        # Verify the prompt passed to the synthesizer contains the search context
        args, kwargs = mock_synthesizer.run_consensus_flow.call_args
        prompt = args[0]
        assert "Real-time Search Data" in prompt
        assert "AI Automation" in prompt

@pytest.mark.asyncio
async def test_market_analyzer_audience_insights():
    """Verify the Audience Insights specialized research."""
    mock_synthesizer = AsyncMock()
    mock_synthesizer.run_consensus_flow.return_value = "Audience Report"
    
    analyzer = MarketAnalyzer(mock_synthesizer)
    
    with patch("src.research.market_analyzer.search_client") as mock_search:
        mock_search.search_market_data = AsyncMock(return_value="Forum Context")
        
        result = await analyzer.get_audience_insights("Biohacking")
        
        assert result == "Audience Report"
        args, kwargs = mock_synthesizer.run_consensus_flow.call_args
        prompt = args[0]
        assert "Forum Context" in prompt
        assert "Biohacking" in prompt
