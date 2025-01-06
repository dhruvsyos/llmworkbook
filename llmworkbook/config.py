"""
Configuration module for LLMs. 
"""

from typing import Optional, Dict

class LLMConfig:
    """
    LLM configuration object to store various LLM parameters.
    """

    def __init__(
        self, 
        provider_name: str = "openai", 
        api_key: Optional[str] = None, 
        model_name: Optional[str] = "gpt-4o-mini",
        system_prompt: Optional[str] = "You're an assistant, process the data for given prompt.", 
        temperature: float = 0.7,
        max_tokens: int = 1024,
        additional_params: Optional[Dict] = None
    ) -> None:
        """
        Initializes the LLM configuration.

        Args:
            provider_name (str): The name of the LLM provider (e.g. "openai", "azure_openai", "cohere").
            api_key (str): The API key to authenticate requests to the LLM provider.
            model_name (str, optional): Model name or version. Default is None.
            system_prompt (str, optional): System-level prompt to guide the LLM. Default is None.
            temperature (float): Sampling temperature to control randomness. Default is 0.7.
            max_tokens (int): Maximum tokens for the output. Default is 1024.
            additional_params (Dict, optional): Any other custom parameters you'd want to pass. Default is None.
        """
        self.provider_name = provider_name
        self.api_key = api_key
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.additional_params = additional_params or {}

    def __repr__(self) -> str:
        return (
            f"LLMConfig(provider_name={self.provider_name}, "
            f"model_name={self.model_name}, temperature={self.temperature}, "
            f"max_tokens={self.max_tokens}, additional_params={self.additional_params})"
        )

