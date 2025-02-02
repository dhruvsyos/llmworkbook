"""
Runner module to handle the actual LLM call.
"""

import os
from typing import Optional
import aiohttp

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

        messages = []
        if self.config.system_prompt:
            messages.append({"role": "system", "content": self.config.system_prompt})
        messages.append({"role": "user", "content": prompt})

        client = OpenAI(api_key=self.config.api_key or os.environ["OPENAI_API_KEY"])

        completion = client.chat.completions.create(
            model=self.config.options["model_name"] or "gpt-4o-mini",
            messages=messages,
            temperature=self.config.options["temperature"],
        )

        try:
            return completion.choices[0].message.content
        except (KeyError, IndexError):
            return str(completion)
        

    async def _call_llm_ollama(self, prompt: str, url: Optional[str]= None) -> str:
        """
        Calls Ollama's completion/chat endpoint asynchronously.

        Args:
            prompt (str): The user prompt to send to the LLM.
            url (str): The URL of the Ollama server.

        Returns:
            str: The LLM response text.
        """
        # Default URL if none is provided
        if url is None:
            url = "http://localhost:11434"  # Default Ollama server URL

        messages = []
        if self.config.system_prompt:
            messages.append({"role": "system", "content": self.config.system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Construct the payload dynamically from self.config.options
        payload = {
            "model": self.config.options.get("model", "default-model"),  # Required
            "prompt": prompt,
            "stream" : False,
        }

        # Add all other valid options from self.config.options to the payload
        valid_options = [
            "suffix", "images", "format", "options", "system", "template", 
            "stream", "raw", "keep_alive", "context"
        ]
        for option in valid_options:
            if option in self.config.options:
                payload[option] = self.config.options[option]


        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f"{url}/api/chat", json=payload) as response:
                    if response.status == 200:
                        completion = await response.json()
                        return completion.get("choices", [{}])[0].get("message", {}).get("content", "")
                    else:
                        return f"Error: {response.status}, {await response.text()}"
            except Exception as e:
                return f"Exception: {str(e)}"

    async def run(self, prompt: str) -> str:
        """
        Entry point for calling any LLM provider.

        Args:
            prompt (str): The user prompt to send to the LLM.

        Returns:
            str: The LLM response text.
        """
        provider = self.config.provider.lower()

        if provider == "openai":
            return await self._call_llm_openai(prompt)
        
        if prompt == "ollama" :
            # Check if 'url' is defined in self.config.options
            url = self.config.options.get("url")

            # Call the function conditionally
            if url:
                return await self._call_llm_ollama(prompt, url=url)
            else:
                return await self._call_llm_ollama(prompt)

        raise NotImplementedError(f"Provider {provider} is not supported yet.")

    @sync_to_async
    async def run_sync(self, prompt: str) -> str:
        """
        Synchronous wrapper for simpler usage.

        Args:
            prompt (str): The user prompt.

        Returns:
            str: The LLM response text.
        """
        return await self.run(prompt)
