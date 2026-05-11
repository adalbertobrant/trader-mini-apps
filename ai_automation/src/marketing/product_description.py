from src.utils.consensus import ConsensusSynthesizer


class ProductDescriptionGenerator:
    """
    Implements the 'Product Description Writer' (Tip 33).
    Turns product features into benefit-focused, conversion-optimized copy.
    """
    def __init__(self, synthesizer: ConsensusSynthesizer):
        self.synthesizer = synthesizer

    async def generate(self, product_name: str, features: str, target_audience: str, platform: str = "website") -> str:
        """
        Generates conversion-optimized product descriptions for a given platform.
        """
        prompt = (
            f"Write conversion-optimized product descriptions for: '{product_name}'.\n\n"
            f"Product Features:\n{features}\n\n"
            f"Target Audience: {target_audience}\n"
            f"Platform: {platform}\n\n"
            f"Deliver 3 variations:\n"
            f"1. **Short (50 words):** Hook + core benefit for ads/social.\n"
            f"2. **Medium (150 words):** For product cards / marketplace listings.\n"
            f"3. **Long (300 words):** Full page copy with features-to-benefits, social proof placeholder, and CTA.\n\n"
            f"Rules: Lead with benefits not features. Use sensory/emotional language. Include SEO keywords naturally."
        )

        system_prompt = (
            "You are a world-class Direct Response Copywriter specializing in e-commerce. "
            "Every word must earn its place. Turn specs into desires. Make the reader feel they need this product."
        )

        return await self.synthesizer.run_consensus_flow(prompt, system_prompt)
