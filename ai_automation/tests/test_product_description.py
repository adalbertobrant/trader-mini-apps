import pytest
from unittest.mock import AsyncMock, patch
from src.marketing.product_description import ProductDescriptionGenerator


@pytest.mark.asyncio
async def test_generate_product_description():
    mock_synthesizer = AsyncMock()
    mock_synthesizer.run_consensus_flow.return_value = "3 Product Description Variations"

    generator = ProductDescriptionGenerator(mock_synthesizer)
    result = await generator.generate(
        product_name="AI Writing Tool",
        features="GPT-4 powered, SEO scoring, 50+ templates",
        target_audience="Freelance content writers",
        platform="website"
    )

    assert result == "3 Product Description Variations"
    args, _ = mock_synthesizer.run_consensus_flow.call_args
    prompt = args[0]
    assert "AI Writing Tool" in prompt
    assert "Freelance content writers" in prompt
    assert "website" in prompt
    assert "Short" in prompt
    assert "Medium" in prompt
    assert "Long" in prompt
