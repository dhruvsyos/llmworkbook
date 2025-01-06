"""
Runner module to handle the actual LLM call.
"""

import asyncio
import aiohttp
from typing import Any, Dict, Optional
from .config import LLMConfig

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

    async def _call_llm_openai(
        self, 
        prompt: str
    ) -> str:
        """
        Calls OpenAI's completion/chat endpoint asynchronously.

        Args:
            prompt (str): The user prompt to send to the LLM.

        Returns:
            str: The LLM response text.
        """
        import os

        # You might want to install openai or call the REST endpoint with your own logic
        # We'll do a sample approach with REST for demonstration
        openai_api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }

        # Build the chat request body
        # For chat completions, we pass 'system' and 'user' messages
        messages = []
        if self.config.system_prompt:
            messages.append({"role": "system", "content": self.config.system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.config.model_name or "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            **self.config.additional_params
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(openai_api_url, json=payload, headers=headers, timeout=60) as resp:
                resp_json = await resp.json()
                # The response structure can vary, but typically you can parse out the text like below
                try:
                    return resp_json["choices"][0]["message"]["content"]
                except (KeyError, IndexError):
                    return str(resp_json)

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
        else:
            # In a real package, you'd add more providers or raise a custom exception
            raise NotImplementedError(f"Provider {provider} is not supported yet.")

    def run_sync(self, prompt: str) -> str:
        """
        Synchronous wrapper for simpler usage.

        Args:
            prompt (str): The user prompt.

        Returns:
            str: The LLM response text.
        """
        return asyncio.run(self.run(prompt))
