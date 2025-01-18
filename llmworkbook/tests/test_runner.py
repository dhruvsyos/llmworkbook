import pandas as pd
from llmworkbook import LLMConfig, LLMRunner, LLMDataFrameIntegrator
import pytest
from unittest.mock import AsyncMock, patch

# def test_llm_runner():


@pytest.fixture
def mock_config():
    """Fixture to provide a mock LLMConfig object."""
    return LLMConfig(
        api_key="mock_api_key",
        provider="openai",
        system_prompt="You are a helpful assistant.",
        options={"model_name": "gpt-4", "temperature": 0.7},
    )

@pytest.mark.asyncio
@patch("llmworkbook.runner.OpenAI")
async def test_call_llm_openai_success(mock_openai, mock_config):
    """
    Test `_call_llm_openai` for a successful response.
    """
    # Mock the OpenAI client and its method
    mock_client = AsyncMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value = {
        "choices": [{"message": "Mocked response"}]
    }

    runner = LLMRunner(mock_config)
    prompt = "Hello, LLM!"
    response = await runner._call_llm_openai(prompt)

    assert response == "Mocked response"
    mock_client.chat.completions.create.assert_called_once_with(
        model="gpt-4",
        messages=[
            {"role": "system", "content": mock_config.system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )


@pytest.mark.asyncio
@patch("llmworkbook.runner.OpenAI")
async def test_call_llm_openai_error_handling(mock_openai, mock_config):
    """
    Test `_call_llm_openai` when an error occurs.
    """
    # Mock the OpenAI client and its method
    mock_client = AsyncMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value = {}

    runner = LLMRunner(mock_config)
    prompt = "Hello, LLM!"
    response = await runner._call_llm_openai(prompt)

    assert response == "{}"  # Expect the string representation of the empty dict
    mock_client.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_run_openai_provider(mock_config):
    """
    Test `run` method for the 'openai' provider.
    """
    runner = LLMRunner(mock_config)
    runner._call_llm_openai = AsyncMock(return_value="Mocked LLM response")
    prompt = "Hello, LLM!"
    response = await runner.run(prompt)

    assert response == "Mocked LLM response"
    runner._call_llm_openai.assert_called_once_with(prompt)


@pytest.mark.asyncio
async def test_run_unsupported_provider(mock_config):
    """
    Test `run` method for unsupported providers.
    """
    mock_config.provider = "unsupported_provider"
    runner = LLMRunner(mock_config)

    with pytest.raises(NotImplementedError) as exc_info:
        await runner.run("Hello, LLM!")

    assert str(exc_info.value) == "Provider unsupported_provider is not supported yet."


@patch("llmworkbook.runner.sync_to_async")
def test_run_sync(mock_sync_to_async, mock_config):
    """
    Test `run_sync` method.
    """
    runner = LLMRunner(mock_config)
    mock_sync_to_async.return_value = AsyncMock(return_value="Mocked Sync Response")

    # Call the method synchronously
    response = runner.run_sync("Hello, LLM!")

    assert response == "Mocked Sync Response"
    mock_sync_to_async.assert_called_once_with(runner.run)
