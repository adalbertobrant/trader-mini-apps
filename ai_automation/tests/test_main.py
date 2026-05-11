import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from main import run_pipeline


@pytest.mark.asyncio
async def test_cli_market_research(capsys):
    """Option 1: market research calls MarketAnalyzer.analyze_niche."""
    mock_synthesizer = MagicMock()

    with patch("main.MultiModelClient"), \
         patch("main.ConsensusSynthesizer", return_value=mock_synthesizer), \
         patch("main.MarketAnalyzer") as MockAnalyzer, \
         patch("builtins.input", side_effect=["1", "AI tools", "0"]):

        mock_instance = AsyncMock()
        mock_instance.analyze_niche.return_value = "Market Report"
        MockAnalyzer.return_value = mock_instance

        await run_pipeline()

    mock_instance.analyze_niche.assert_called_once_with("AI tools")
    captured = capsys.readouterr()
    assert "Market Report" in captured.out


@pytest.mark.asyncio
async def test_cli_full_pipeline(capsys):
    """Option 6: full pipeline calls analyzer then writer in sequence."""
    mock_synthesizer = MagicMock()

    with patch("main.MultiModelClient"), \
         patch("main.ConsensusSynthesizer", return_value=mock_synthesizer), \
         patch("main.MarketAnalyzer") as MockAnalyzer, \
         patch("main.SEOWriter") as MockWriter, \
         patch("builtins.input", side_effect=["6", "SaaS", "Best CRM tools 2026", "n", "0"]):
        mock_analyzer = AsyncMock()
        mock_analyzer.analyze_niche.return_value = "Research Data"
        MockAnalyzer.return_value = mock_analyzer

        mock_writer = AsyncMock()
        mock_writer.write_article.return_value = "SEO Article"
        MockWriter.return_value = mock_writer

        await run_pipeline()

    mock_analyzer.analyze_niche.assert_called_once_with("SaaS")
    mock_writer.write_article.assert_called_once_with("Best CRM tools 2026", "Research Data")
    captured = capsys.readouterr()
    assert "SEO Article" in captured.out
