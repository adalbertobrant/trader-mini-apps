from typing import Dict, Optional
from src.utils.ai_client import MultiModelClient

class ConsensusSynthesizer:
    """
    Synthesizes multiple AI responses into a single 'Gold Standard' output.
    Uses a primary model to judge and merge the contributions of other models.
    """
    def __init__(self, multi_client: MultiModelClient):
        self.multi_client = multi_client
        # We prefer a highly analytical model for the final synthesis
        self.primary_model_name = "anthropic" 

    async def synthesize(self, original_prompt: str, responses: Dict[str, str]) -> str:
        """
        Takes the original prompt and all model responses to create a final synthesized version.
        """
        if not responses:
            return "Error: No responses provided for synthesis."

        # Prepare the synthesis prompt
        synthesis_input = "\n\n".join([f"### Model: {name}\n{output}" for name, output in responses.items()])
        
        system_prompt = (
            "You are an expert SEO Synthesizer. Your job is to take multiple AI-generated responses "
            "and merge them into a single, superior 'Gold Standard' output. "
            "1. Identify the most accurate facts across all responses.\n"
            "2. Adopt the best writing style and structure identified.\n"
            "3. Ensure all target keywords are naturally integrated.\n"
            "4. Eliminate redundancies and hallucinations.\n"
            "Output ONLY the final synthesized content."
        )

        synthesis_prompt = (
            f"Original Task: {original_prompt}\n\n"
            f"Here are the responses from different AI models:\n\n"
            f"{synthesis_input}\n\n"
            f"Based on the above, provide the final optimized version:"
        )

        # Use the primary client if it responded successfully, otherwise fall back
        # to any client that actually produced a valid response.
        if self.primary_model_name in responses:
            primary_client = self.multi_client.clients[self.primary_model_name]
        else:
            first_valid = next(iter(responses))
            primary_client = self.multi_client.clients[first_valid]

        return await primary_client.generate_text(synthesis_prompt, system_prompt)

    async def run_consensus_flow(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Helper method to run the full flow: Query All -> Synthesize.
        """
        responses = await self.multi_client.query_all(prompt, system_prompt)
        # Filter out errors from the synthesis input
        valid_responses = {name: res for name, res in responses.items() if not res.startswith("Error:")}
        
        if not valid_responses:
            return "Error: All models failed to respond."
            
        return await self.synthesize(prompt, valid_responses)
