import abc
import asyncio
from typing import Optional, Dict
import anthropic
from google import genai
from groq import AsyncGroq
from mistralai.client import Mistral
from openai import AsyncOpenAI
from src.utils.config import config

class BaseAIClient(abc.ABC):
    """Abstract base class for all AI model providers."""
    @abc.abstractmethod
    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        pass

class AnthropicClient(BaseAIClient):
    def __init__(self, api_key: str):
        self.client = anthropic.AsyncAnthropic(api_key=api_key)

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        message = await self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            system=system_prompt or "",
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

class GeminiClient(BaseAIClient):
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        # google-genai handles system instructions in the generate call or config
        response = await self.client.aio.models.generate_content(
            model="gemini-1.5-pro",
            contents=prompt,
            config={"system_instruction": system_prompt} if system_prompt else None
        )
        return response.text

class GroqClient(BaseAIClient):
    def __init__(self, api_key: str):
        self.client = AsyncGroq(api_key=api_key)

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        completion = await self.client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages
        )
        return completion.choices[0].message.content

class MistralClient(BaseAIClient):
    def __init__(self, api_key: str):
        self.client = Mistral(api_key=api_key)

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = await self.client.chat.complete_async(
            model="mistral-large-latest",
            messages=messages
        )
        return response.choices[0].message.content

class OpenRouterClient(BaseAIClient):
    """OpenRouter client — routes to 200+ models via a single OpenAI-compatible endpoint."""
    def __init__(self, api_key: str, model: str = "openai/gpt-4o-mini"):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = model

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion.choices[0].message.content

class LocalAIClient(BaseAIClient):
    def __init__(self, base_url: str, model: str):
        self.client = AsyncOpenAI(base_url=base_url, api_key="sk-no-key-required")
        self.model = model

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion.choices[0].message.content

class MultiModelClient:
    """Orchestrator for querying multiple AI models."""
    def __init__(self):
        self.clients: Dict[str, BaseAIClient] = {}
        self._initialize_clients()

    def _initialize_clients(self):
        if config.ANTHROPIC_API_KEY:
            self.clients["anthropic"] = AnthropicClient(config.ANTHROPIC_API_KEY)
        if config.GOOGLE_API_KEY:
            self.clients["gemini"] = GeminiClient(config.GOOGLE_API_KEY)
        if config.GROQ_API_KEY:
            self.clients["groq"] = GroqClient(config.GROQ_API_KEY)
        if config.MISTRAL_API_KEY:
            self.clients["mistral"] = MistralClient(config.MISTRAL_API_KEY)
        if config.OPENROUTER_API_KEY:
            self.clients["openrouter"] = OpenRouterClient(config.OPENROUTER_API_KEY)
        
        # LocalAI is always available if configured
        self.clients["local"] = LocalAIClient(config.LOCAL_AI_BASE_URL, config.LOCAL_AI_MODEL)

    async def query_all(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, str]:
        """Query all available models truly concurrently and return results.

        Concurrency model: asyncio-based (single event loop, cooperative multitasking).
        This is safe for concurrent async use — multiple coroutines can call this
        simultaneously on the same event loop without data races, as there is no
        shared mutable state.

        Thread-safety caveat: if called from multiple OS threads, each thread MUST
        run its own event loop (e.g. via asyncio.run()). Sharing one event loop
        across threads is not supported by asyncio and will cause undefined behavior.
        For the current single-process use case this is not a concern.
        """
        names = list(self.clients.keys())
        tasks = [self.clients[name].generate_text(prompt, system_prompt) for name in names]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return {
            name: f"Error: {r}" if isinstance(r, Exception) else r
            for name, r in zip(names, responses)
        }
