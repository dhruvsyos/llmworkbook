"""
Integrator module to combine LLM responses and DataFrames.
"""

from typing import Optional, List, Union

import asyncio
import pandas as pd

from .runner import LLMRunner


class LLMDataFrameIntegrator:
    """
    Integrates LLM calls with a DataFrame.
    """

    def __init__(self, runner: LLMRunner, df: pd.DataFrame) -> None:
        """
        Args:
            runner (LLMRunner): The runner object to call the LLM.
            df (pd.DataFrame): The DataFrame to attach results to.
        """
        self.runner = runner
        self.df = df

    def add_llm_responses(
        self,
        prompt_column: str = "prompt_column",
        response_column: str = "llm_response",
        row_filter: Optional[List[int]] = None,
        async_mode: bool = False,
    ) -> pd.DataFrame:
        """
        Runs the LLM on each row's `prompt_column` text and stores the response in
        `response_column`.

        Args:
            prompt_column (str): The column in the DataFrame containing prompt text.
            response_column (str, optional): The name of the column to store LLM responses.
                                            Defaults to "llm_response".
            row_filter (List[int], optional): Subset of row indices to run.
                                            If None, runs on all rows.
            async_mode (bool, optional): If True, uses async calls to LLM. Otherwise uses sync.

        Returns:
            pd.DataFrame: The updated DataFrame with responses.
        """
        if response_column not in self.df.columns:
            self.df[response_column] = None

        if row_filter is None:
            row_indices = self.df.index.tolist()
        else:
            row_indices = row_filter

        if async_mode:
            return self._run_async_prompts(row_indices, prompt_column, response_column)

        for idx in row_indices:
            prompt_value = self.df.at[idx, prompt_column]
            if prompt_value:
                response = self.runner.run_sync(str(prompt_value))
                self.df.at[idx, response_column] = response
        return self.df

    def reset_responses(self, response_column: str = "llm_response") -> pd.DataFrame:
        """
        Resets the response column in the DataFrame by setting it to None.

        Args:
            response_column (str, optional): The name of the column to reset.

        Returns:
            pd.DataFrame: The updated DataFrame with the response column reset.
        """
        if response_column in self.df.columns:
            self.df[response_column] = None
        return self.df

    def _run_async_prompts(
        self, row_indices: List[int], prompt_column: str, response_column: str
    ) -> pd.DataFrame:
        """
        Helper method that runs LLM calls asynchronously in parallel.
        """

        async def process_row(idx: Union[int, str]) -> None:
            prompt_value = self.df.at[idx, prompt_column]
            if prompt_value:
                response = await self.runner.run(str(prompt_value))
                self.df.at[idx, response_column] = response

        async def main():
            tasks = [process_row(idx) for idx in row_indices]
            await asyncio.gather(*tasks)

        asyncio.run(main())
        return self.df
