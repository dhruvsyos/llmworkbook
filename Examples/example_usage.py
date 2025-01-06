"""
Example usage script.
"""

import pandas as pd
from llmworkbook import LLMConfig, LLMRunner, LLMDataFrameIntegrator

def main():
    # 1. Create a sample dataframe
    data = {
        "id": [1, 2, 3],
        "prompt_text": [
            "Explain Newton's first law in simple terms.",
            "Write a short poem about the moon.",
            "Give me 3 tips for better time management."
        ]
    }
    df = pd.DataFrame(data)

    # 2. Create an LLM configuration
    config = LLMConfig(
        provider_name="openai",
        api_key="YOUR_API_KEY",  # Replace with real key
        model_name="gpt-3.5-turbo",
        system_prompt="You are a helpful assistant.",
        temperature=0.5,
        max_tokens=1000
    )

    # 3. Instantiate the runner and the integrator
    runner = LLMRunner(config)
    integrator = LLMDataFrameIntegrator(runner=runner, df=df)

    # 4. Add LLM responses to the df
    updated_df = integrator.add_llm_responses(
        prompt_column="prompt_text",
        response_column="llm_response",
        async_mode=False
    )

    print("DataFrame with LLM responses:\n", updated_df)


if __name__ == "__main__":
    main()
