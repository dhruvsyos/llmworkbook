# pylint: skip-file
import pandas as pd
from pandas.errors import InvalidColumnName
import numpy as np
from llmworkbook import WrapDataFrame, WrapDataArray, WrapPromptList
from unittest.mock import patch
import pytest
from io import StringIO


@pytest.fixture
def sample_dataframe():
    return {
        "prompt": ["Summarize this", "Translate this", "Analyze sentiment"],
        "Reviews": ["Great product", "Muy bueno", "Terrible experience"],
        "Language": ["en", "es", "en"],
    }


def test_transform_and_export_csv(sample_dataframe):
    df = pd.DataFrame(sample_dataframe)
    wrapper = WrapDataFrame(
        df, prompt_column="prompt", data_columns=["Reviews", "Language"]
    )

    with patch.object(pd.DataFrame, "to_csv") as mock_to_csv:
        wrapper.transform_and_export("test_output.csv", "csv")
        mock_to_csv.assert_called_once_with("test_output.csv", index=False)


def test_transform_and_export_json(sample_dataframe):
    df = pd.DataFrame(sample_dataframe)
    wrapper = WrapDataFrame(
        df, prompt_column="prompt", data_columns=["Reviews", "Language"]
    )

    with patch.object(pd.DataFrame, "to_json") as mock_to_json:
        wrapper.transform_and_export("test_output.json", "json")
        mock_to_json.assert_called_once_with("test_output.json", orient="records")


def test_transform_and_export_excel(sample_dataframe):
    df = pd.DataFrame(sample_dataframe)
    wrapper = WrapDataFrame(
        df, prompt_column="prompt", data_columns=["Reviews", "Language"]
    )

    with patch.object(pd.DataFrame, "to_excel") as mock_to_excel:
        wrapper.transform_and_export("test_output.xlsx", "excel")
        mock_to_excel.assert_called_once_with(
            "test_output.xlsx", index=False, engine="openpyxl"
        )


def test_transform_and_export_invalid_format(sample_dataframe):
    df = pd.DataFrame(sample_dataframe)
    wrapper = WrapDataFrame(
        df, prompt_column="prompt", data_columns=["Reviews", "Language"]
    )

    with pytest.raises(ValueError, match="Unsupported file format"):
        wrapper.transform_and_export("test_output.xml", "xml")


def test_preview(sample_dataframe):
    df = pd.DataFrame(sample_dataframe)
    wrapper = WrapDataFrame(
        df, prompt_column="prompt", data_columns=["Reviews", "Language"]
    )

    wrapper.preview(1)
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        output = mock_stdout.getvalue()

    assert output == ""


def test_wrap_dataframe(sample_dataframe):
    df = pd.DataFrame(sample_dataframe)
    wrapper = WrapDataFrame(
        df, prompt_column="prompt", data_columns=["Reviews", "Language"]
    )

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


def test_wrap_dataframe_invalid_column(sample_dataframe):
    df = pd.DataFrame(sample_dataframe)
    # Test data column
    with pytest.raises(InvalidColumnName):
        WrapDataFrame(
            df, prompt_column="prompt", data_columns=["not_existing_col", "Language"]
        )

    # Test prompt column
    with pytest.raises(InvalidColumnName):
        WrapDataFrame(
            df, prompt_column="not_existing_col", data_columns=["Review", "Language"]
        )


@pytest.fixture
def sample_array():
    return np.array(
        [
            ["Summarize this", "Great product", "en"],
            ["Translate this", "Muy bueno", "es"],
            ["Analyze sentiment", "Terrible experience", "en"],
        ]
    )


def test_wrap_data_array(sample_array):
    # Arrange
    wrapper = WrapDataArray(sample_array, prompt_index=0, data_indices=[1, 2])

    # Act
    wrapped_df = wrapper.wrap()

    # Assert
    assert "wrapped_output" in wrapped_df.columns
    assert len(wrapped_df) == len(sample_array)
    expected_first_row = (
        "<data>\n"
        "  <cell>Great product</cell>\n"
        "  <cell>en</cell>\n"
        "</data>"
        "<prompt>Summarize this</prompt>"
    )
    assert wrapped_df.iloc[0, 0] == expected_first_row


def test_array_size():
    with pytest.raises(ValueError):
        data = np.array(["Summarize this", "Great product", "en"])
        WrapDataArray(data)


def test_valid_indices(sample_array):
    # Test data column
    with pytest.raises(IndexError):
        WrapDataArray(sample_array, prompt_index=0, data_indices=[2, 3])

    # Test data column
    with pytest.raises(IndexError):
        WrapDataArray(sample_array, prompt_index=3, data_indices=[1, 2])


@pytest.fixture
def sample_list():
    return ["Summarize this", "Translate this", "Analyze sentiment"]


def test_wrap_prompt_list(sample_list):
    # Arrange
    wrapper = WrapPromptList(sample_list)

    # Act
    wrapped_df = wrapper.wrap()

    # Assert
    assert "wrapped_output" in wrapped_df.columns
    assert len(wrapped_df) == len(sample_list)
    expected_first_row = "<data></data><prompt>Summarize this</prompt>"
    assert wrapped_df.iloc[0, 0] == expected_first_row
