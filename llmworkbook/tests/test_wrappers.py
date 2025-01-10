import pandas as pd
import numpy as np
from llmworkbook import WrapDataFrame, WrapDataArray, WrapPromptList


def test_wrap_dataframe():
    # Arrange
    data = {
        "prompt": ["Summarize this", "Translate this", "Analyze sentiment"],
        "Reviews": ["Great product", "Muy bueno", "Terrible experience"],
        "Language": ["en", "es", "en"]
    }
    df = pd.DataFrame(data)
    wrapper = WrapDataFrame(df, prompt_column="prompt", data_columns=["Reviews", "Language"])
    
    # Act
    wrapped_df = wrapper.wrap()
    
    # Assert
    assert "wrapped_output" in wrapped_df.columns
    assert len(wrapped_df) == len(df)
    expected_first_row = (
        "<data>\n"
        "  <cell>Great product</cell>\n"
        "  <cell>en</cell>\n"
        "</data>"
        "<prompt>Summarize this</prompt>"
    )
    assert wrapped_df.iloc[0, 0] == expected_first_row


def test_wrap_data_array():
    # Arrange
    data = np.array([
        ["Summarize this", "Great product", "en"],
        ["Translate this", "Muy bueno", "es"],
        ["Analyze sentiment", "Terrible experience", "en"]
    ])
    wrapper = WrapDataArray(data, prompt_index=0, data_indices=[1, 2])
    
    # Act
    wrapped_df = wrapper.wrap()
    
    # Assert
    assert "wrapped_output" in wrapped_df.columns
    assert len(wrapped_df) == len(data)
    expected_first_row = (
        "<data>\n"
        "  <cell>Great product</cell>\n"
        "  <cell>en</cell>\n"
        "</data>"
        "<prompt>Summarize this</prompt>"
    )
    assert wrapped_df.iloc[0, 0] == expected_first_row


def test_wrap_prompt_list():
    # Arrange
    prompts = ["Summarize this", "Translate this", "Analyze sentiment"]
    wrapper = WrapPromptList(prompts)
    
    # Act
    wrapped_df = wrapper.wrap()
    
    # Assert
    assert "wrapped_output" in wrapped_df.columns
    assert len(wrapped_df) == len(prompts)
    expected_first_row = "<data></data><prompt>Summarize this</prompt>"
    assert wrapped_df.iloc[0, 0] == expected_first_row

