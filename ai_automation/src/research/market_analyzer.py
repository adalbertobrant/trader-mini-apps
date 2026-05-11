from typing import Optional
from src.utils.consensus import ConsensusSynthesizer
from src.utils.search_client import search_client

class MarketAnalyzer:
    """
    Implements the 'Market Research Report' (Tip 13) and 'Audience Research Engine' (Tip 19).
    Uses consensus-based analysis on top of real-time search data.
    """
    def __init__(self, synthesizer: ConsensusSynthesizer):
        self.synthesizer = synthesizer

    async def analyze_niche(self, niche: str) -> str:
        """
        Performs a full market research analysis for a specific niche.
        """
        # Step 1: Get real-time data from Tavily
        search_query = f"top competitors and audience pain points in the {niche} niche 2024-2026"
        market_context = "No real-time data available (Tavily not configured)."
        
        if search_client:
            market_context = await search_client.search_market_data(search_query)

        # Step 2: Formulate the prompt for the AI swarm
        prompt = (
            f"Perform a deep market research analysis for the niche: '{niche}'.\n\n"
            f"Use the following real-time search context to inform your report:\n"
            f"{market_context}\n\n"
            f"Your report MUST include:\n"
            f"1. **Market Landscape:** Who are the current leaders and emerging players?\n"
            f"2. **Audience Pain Points:** What are customers complaining about in forums and reviews?\n"
            f"3. **Competitor Gaps:** What are they missing that we can solve?\n"
            f"4. **SEO Keywords:** Identify 5 high-potential 'low-hanging fruit' keyword themes.\n"
            f"5. **Recommended Angle:** A unique selling proposition for a new product/service."
        )

        system_prompt = (
            "You are a Senior Market Research Strategist. Use the provided search context "
            "to create a data-driven, actionable report. Be specific, avoid generic advice, "
            "and prioritize opportunities with high revenue potential."
        )

        # Step 3: Run through the consensus flow
        return await self.synthesizer.run_consensus_flow(prompt, system_prompt)

    async def get_audience_insights(self, niche: str) -> str:
        """
        Focuses specifically on Audience Research (Tip 19).
        """
        search_query = f"what is the audience asking about in {niche} forums reddit 2026"
        audience_context = "No real-time data available."
        
        if search_client:
            audience_context = await search_client.search_market_data(search_query)

        prompt = (
            f"Analyze the audience for: '{niche}'.\n\n"
            f"Research Context:\n{audience_context}\n\n"
            f"Identify the Top 5 most frequent questions and 'hidden desires' of this audience. "
            "Format each insight as: 'Question/Desire' followed by 'Why it matters' and 'Content Opportunity'."
        )

        return await self.synthesizer.run_consensus_flow(prompt)
