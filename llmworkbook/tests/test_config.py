from llmworkbook import LLMConfig

def test_llm_config_initialization():
    # Arrange
    config = LLMConfig(
        provider="openai",
        system_prompt="You are a helpful assistant.",
        options={
            "model_name": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 1000,
        },
    )

    # Assert
    assert config.provider == "openai"
    assert config.options["model_name"] == "gpt-3.5-turbo"
    assert config.system_prompt == "You are a helpful assistant."
    assert config.options["temperature"] == 0.7
    assert config.options["max_tokens"] == 1000

    #Arrange
    results = config.to_dict()

    #Assert
    assert results["provider"] == "openai"
    assert results["system_prompt"] == "You are a helpful assistant."
    assert results["options"] == {
            "model_name": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 1000,
        }

