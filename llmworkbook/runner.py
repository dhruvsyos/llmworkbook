"""
Runner module to handle the actual LLM call.
"""
import os

from openai import OpenAI

from .config import LLMConfig
from .utils import sync_to_async


class LLMRunner:
    """
    LLMRunner handles calling the LLM provider using the configuration.
    """

    def __init__(self, config: LLMConfig) -> None:
        """
        Args:
            config (LLMConfig): The configuration object for the LLM.
        """
        self.config = config

    async def _call_llm_openai(self, prompt: str) -> str:
        """
        Calls OpenAI's completion/chat endpoint asynchronously.

        Args:
            prompt (str): The user prompt to send to the LLM.

        Returns:
            str: The LLM response text.
        """
        from openai import OpenAI

        messages = []
        if self.config.system_prompt:
            messages.append({"role": "system", "content": self.config.system_prompt})
        messages.append({"role": "user", "content": prompt})

        client = OpenAI(api_key=self.config.api_key or os.environ["OPENAAI_API_KEY"])

        completion = client.chat.completions.create(
            model=self.config.model_name or "gpt-4o-mini",
            messages=messages,
            temperature=self.config.temperature,
        )

        try:
            return completion.choices[0].message
        except (KeyError, IndexError):
            return str(completion)

    async def run(self, prompt: str) -> str:
        """
        Entry point for calling any LLM provider.

        Args:
            prompt (str): The user prompt to send to the LLM.

        Returns:
            str: The LLM response text.
        """
        provider = self.config.provider_name.lower()

        if provider == "openai":
            return await self._call_llm_openai(prompt)
        raise NotImplementedError(f"Provider {provider} is not supported yet.")

    def run_sync(self, prompt: str) -> str:
        """
        Synchronous wrapper for simpler usage.

        Args:
            prompt (str): The user prompt.

        Returns:
            str: The LLM response text.
        """
        return await self.run(prompt)
