#!/usr/bin/env python3

"""
CLI for LLMWorkbook Wrappers
"""

import argparse
import pandas as pd
import numpy as np
import json
from llmworkbook import WrapDataFrame, WrapDataArray, WrapPromptList


def wrap_dataframe(input_file, output_file, prompt_column, data_columns):
    """
    Wrap a DataFrame and save the output.
    """
    df = pd.read_csv(input_file) if input_file.endswith(".csv") else pd.read_excel(input_file)
    wrapper = WrapDataFrame(df, prompt_column=prompt_column, data_columns=data_columns.split(","))
    wrapped_df = wrapper.wrap()
    wrapped_df.to_csv(output_file, index=False)
    print(f"Wrapped DataFrame saved to {output_file}")


def wrap_array(input_file, output_file, prompt_index, data_indices):
    """
    Wrap a 2D array and save the output.
    """
    with open(input_file, "r") as file:
        array_data = json.load(file)  # Expecting a JSON file with a list of lists
    wrapper = WrapDataArray(np.array(array_data), prompt_index=int(prompt_index), data_indices=[int(idx) for idx in data_indices.split(",")])
    wrapped_df = wrapper.wrap()
    wrapped_df.to_csv(output_file, index=False)
    print(f"Wrapped Array saved to {output_file}")


def wrap_prompts(prompts_file, output_file):
    """
    Wrap a list of prompts and save the output.
    """
    with open(prompts_file, "r") as file:
        prompts = file.readlines()  # Assuming one prompt per line
    wrapper = WrapPromptList([prompt.strip() for prompt in prompts])
    wrapped_df = wrapper.wrap()
    wrapped_df.to_csv(output_file, index=False)
    print(f"Wrapped Prompts saved to {output_file}")


def main():
    """
    Main function to handle CLI arguments and dispatch commands.
    """
    parser = argparse.ArgumentParser(
        description="CLI for wrapping data for LLMWorkbook."
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    # Sub-command: wrap_dataframe
    parser_df = subparsers.add_parser("wrap_dataframe", help="Wrap a pandas DataFrame")
    parser_df.add_argument("input_file", help="Path to the input file (CSV/Excel)")
    parser_df.add_argument("output_file", help="Path to save the wrapped output (CSV)")
    parser_df.add_argument("prompt_column", help="Column name for the prompt")
    parser_df.add_argument(
        "data_columns", help="Comma-separated column names for the data to wrap"
    )

    # Sub-command: wrap_array
    parser_array = subparsers.add_parser("wrap_array", help="Wrap a 2D array")
    parser_array.add_argument("input_file", help="Path to the JSON file with array data")
    parser_array.add_argument("output_file", help="Path to save the wrapped output (CSV)")
    parser_array.add_argument("prompt_index", help="Index of the prompt column in the array")
    parser_array.add_argument("data_indices", help="Comma-separated indices for data columns")

    # Sub-command: wrap_prompts
    parser_prompts = subparsers.add_parser("wrap_prompts", help="Wrap a list of prompts")
    parser_prompts.add_argument("prompts_file", help="Path to the file containing prompts (one per line)")
    parser_prompts.add_argument("output_file", help="Path to save the wrapped output (CSV)")

    # Parse arguments
    args = parser.parse_args()

    # Dispatch commands
    if args.command == "wrap_dataframe":
        wrap_dataframe(args.input_file, args.output_file, args.prompt_column, args.data_columns)
    elif args.command == "wrap_array":
        wrap_array(args.input_file, args.output_file, args.prompt_index, args.data_indices)
    elif args.command == "wrap_prompts":
        wrap_prompts(args.prompts_file, args.output_file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
