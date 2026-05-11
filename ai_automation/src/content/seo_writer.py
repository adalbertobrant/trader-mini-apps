from typing import Optional
from src.utils.consensus import ConsensusSynthesizer

class SEOWriter:
    """
    Implements the 'SEO Article Writer' (Tip 05).
    Uses consensus-based writing to ensure optimal keyword density, structure, and readability.
    """
    def __init__(self, synthesizer: ConsensusSynthesizer):
        self.synthesizer = synthesizer

    async def write_article(self, topic: str, research_context: str) -> str:
        """
        Generates a full SEO-optimized article based on a topic and research data.
        """
        prompt = (
            f"Write a comprehensive, SEO-optimized blog post about: '{topic}'.\n\n"
            f"Use the following market research and context to guide the content:\n"
            f"{research_context}\n\n"
            f"Your article MUST follow these SEO requirements:\n"
            f"1. **Semantic Structure:** Use a clear H1, multiple H2s, and H3s for readability.\n"
            f"2. **Keyword Integration:** Naturally weave in the high-potential keywords identified in the research.\n"
            f"3. **Value-First Content:** Address the specific audience pain points mentioned in the context.\n"
            f"4. **Formatting:** Use bullet points, bold text for emphasis, and short paragraphs.\n"
            f"5. **Meta Data:** Include a compelling SEO Title (max 60 chars) and Meta Description (max 155 chars).\n"
            f"6. **Internal Linking:** Suggest 3 logical places for internal links (use placeholders like [Internal Link: Topic])."
        )

        system_prompt = (
            "You are a World-Class SEO Content Specialist and Copywriter. "
            "Your goal is to write content that not only ranks #1 on Google but also provides "
            "immense value to the reader. Avoid fluff, be authoritative, and maintain an engaging tone."
        )

        # Run through the consensus flow to get the 'Gold Standard' article
        return await self.synthesizer.run_consensus_flow(prompt, system_prompt)

    async def generate_seo_meta(self, article_content: str) -> str:
        """
        Refines or generates SEO meta data specifically for an existing piece of content.
        """
        prompt = (
            f"Based on the following article content, generate 3 variations of SEO Titles and Meta Descriptions:\n\n"
            f"{article_content[:2000]}..." # Use first 2k chars for context
        )
        
        system_prompt = "You are an SEO Meta Data Expert. Focus on curiosity gaps and high CTR (Click-Through Rate) frameworks."
        
        return await self.synthesizer.run_consensus_flow(prompt, system_prompt)
