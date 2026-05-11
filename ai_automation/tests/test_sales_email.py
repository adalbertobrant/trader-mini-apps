import pytest
from unittest.mock import AsyncMock, patch
from src.marketing.sales_email import SalesEmailPersonalizer


@pytest.mark.asyncio
async def test_generate_email_with_search():
    mock_synthesizer = AsyncMock()
    mock_synthesizer.run_consensus_flow.return_value = "Personalized Cold Email"

    personalizer = SalesEmailPersonalizer(mock_synthesizer)

    with patch("src.marketing.sales_email.search_client") as mock_search:
        mock_search.search_market_data = AsyncMock(return_value="Company has thin blog content")

        result = await personalizer.generate_email("Acme Corp", "SEO Content Writing")

        assert result == "Personalized Cold Email"
        args, _ = mock_synthesizer.run_consensus_flow.call_args
        prompt = args[0]
        assert "Acme Corp" in prompt
        assert "SEO Content Writing" in prompt
        assert "Company has thin blog content" in prompt


@pytest.mark.asyncio
async def test_generate_batch():
    mock_synthesizer = AsyncMock()
    mock_synthesizer.run_consensus_flow.return_value = "Email"

    personalizer = SalesEmailPersonalizer(mock_synthesizer)

    with patch("src.marketing.sales_email.search_client", None):
        results = await personalizer.generate_batch(["CompanyA", "CompanyB"], "SEO Services")

    assert set(results.keys()) == {"CompanyA", "CompanyB"}
    assert all(v == "Email" for v in results.values())
