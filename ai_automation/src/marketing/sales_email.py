import asyncio
from src.utils.consensus import ConsensusSynthesizer
from src.utils.search_client import search_client


class SalesEmailPersonalizer:
    """
    Implements the 'Sales Email Personalizer' (Tip 35).
    Researches each prospect via Tavily and writes a personalized cold email.
    """
    def __init__(self, synthesizer: ConsensusSynthesizer):
        self.synthesizer = synthesizer

    async def generate_email(self, company_name: str, service_offered: str) -> str:
        """
        Researches a prospect company and writes a personalized cold outreach email.
        """
        company_context = "No real-time data available (Tavily not configured)."
        if search_client:
            company_context = await search_client.search_market_data(
                f"{company_name} blog content gaps SEO weaknesses 2026"
            )

        prompt = (
            f"Write a personalized cold outreach email to a prospect at: '{company_name}'.\n\n"
            f"Service we're offering: {service_offered}\n\n"
            f"Research context about the company:\n{company_context}\n\n"
            f"Email requirements:\n"
            f"1. Subject line: Specific, curiosity-driven, no spam words.\n"
            f"2. Opening: Reference something specific about their business from the research.\n"
            f"3. Pain point: Identify one clear content/SEO gap they have.\n"
            f"4. Value proposition: How our service solves that specific gap.\n"
            f"5. CTA: One low-friction ask (e.g., 15-min call or free audit).\n"
            f"6. Tone: Peer-to-peer, not salesy. Under 150 words total."
        )

        system_prompt = (
            "You are an expert B2B sales copywriter. Write emails that feel like they came from "
            "a knowledgeable peer, not a vendor. Be specific, be brief, be human."
        )

        return await self.synthesizer.run_consensus_flow(prompt, system_prompt)

    async def generate_batch(self, companies: list[str], service_offered: str) -> dict[str, str]:
        """
        Generates personalized emails for a list of companies concurrently.
        """
        tasks = [self.generate_email(company, service_offered) for company in companies]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return {
            company: f"Error: {r}" if isinstance(r, Exception) else r
            for company, r in zip(companies, results)
        }
