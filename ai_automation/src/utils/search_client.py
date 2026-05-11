from tavily import AsyncTavilyClient
from src.utils.config import config

class TavilySearch:
    """
    Wrapper for Tavily Search API to provide real-time context to the AI swarm.
    """
    def __init__(self, api_key: str):
        self.client = AsyncTavilyClient(api_key=api_key)

    async def search_market_data(self, query: str) -> str:
        """
        Performs a deep search for market research data and returns a formatted summary.
        """
        search_result = await self.client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=True
        )
        
        # Combine the AI-generated answer with snippets from top results
        answer = search_result.get("answer", "No direct answer found.")
        results = search_result.get("results", [])
        
        snippets = "\n\n".join([
            f"Source: {res['url']}\nSnippet: {res['content']}" 
            for res in results
        ])
        
        return f"### Tavily AI Answer:\n{answer}\n\n### Top Search Context:\n{snippets}"

# Global instance
search_client = None
if config.TAVILY_API_KEY:
    search_client = TavilySearch(config.TAVILY_API_KEY)
