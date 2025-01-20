import pytest
from unittest.mock import AsyncMock, patch
from llmworkbook import LLMRunner, LLMConfig
from openai import OpenAI

@pytest.fixture
def mock_config():
    """Fixture for creating an LLMConfig object."""
    return LLMConfig(
        provider="openai",
        api_key="test-api-key",
        system_prompt="Process these Data rows as per the provided prompt",
        options={
            "model_name": "gpt-4o-mini",
            "temperature": 1,
            "max_tokens": 1024,
        },
    )


@pytest.mark.asyncio
async def test_llmrunner_initialization(mock_config):
    """Test that LLMRunner initializes correctly."""
    runner = LLMRunner(config=mock_config)
    assert runner.config == mock_config


@pytest.mark.asyncio
async def test_run(mock_config):
    """Test the run method with the OpenAI provider (async)."""
    runner = LLMRunner(config=mock_config)

    # Mock the internal method that actually calls OpenAI
    runner._call_llm_openai = AsyncMock(return_value="LLM response for prompt")
    
    # Invoke async method
    result = await runner.run("Explain Newton's first law in simple terms.")
    
    # Validate result
    assert result == "LLM response for prompt"
    runner._call_llm_openai.assert_called_once_with("Explain Newton's first law in simple terms.")


def test_run_sync(mock_config):
    """
    Test the synchronous wrapper for the run method.

    NOTE: This test is a normal, synchronous function. 
    It should NOT be marked as async or use the @pytest.mark.asyncio decorator.
    """
    runner = LLMRunner(config=mock_config)

    # Mock the async run method
    runner.run = AsyncMock(return_value="Sync response")
    
    # Call the sync method
    result = runner.run_sync("Explain Newton's first law in simple terms.")
    
    # Validate result
    assert result == "Sync response"
    runner.run.assert_called_once_with("Explain Newton's first law in simple terms.")


@pytest.mark.asyncio
async def test_provider():
    """Test behavior for an unsupported provider."""
    with pytest.raises(NotImplementedError):
        await LLMRunner(config=LLMConfig(provider="llmprovider")).run("prompt")


@pytest.mark.asyncio
async def test_call_llm_openai(mock_config):
    """Test the _call_llm_openai method with a mocked OpenAI response."""
    runner = LLMRunner(config=mock_config)

    # Mocked response from OpenAI API
    mock_response = AsyncMock()
    mock_response.choices[0].message = "Mocked response text"

    # Patch the OpenAI client and its chat completion method
    with patch.object(OpenAI, "chat", create=True) as mock_chat:
        # Mock the completions.create method
        mock_chat.completions.create.return_value = mock_response

        response = await runner._call_llm_openai("Test prompt")

        assert response == "Mocked response text"
        mock_chat.completions.create.assert_called_once_with(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": mock_config.system_prompt},
                {"role": "user", "content": "Test prompt"}
            ],
            temperature=mock_config.options["temperature"],
        )
