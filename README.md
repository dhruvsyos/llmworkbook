# **LLMWorkbook**

> [!WARNING]
> This repo is in development and may not be secure. Use is at your own risk

**LLMWorkbook** is a Python package designed to seamlessly integrate Large Language Models (LLMs) into your workflow with DataFrames. This package allows you to easily configure an LLM, send prompts **row-wise** from a DataFrame, and store responses back in the DataFrame with minimal effort.

---

## **Features**

- Configure LLM providers (e.g., OpenAI) using a simple configuration object.
- Asynchronous and synchronous support for LLM calls.
- Easily map LLM responses to a specific column in a pandas DataFrame.
- Extendable architecture for multiple LLM providers.
- Built-in utilities for preprocessing and handling API limits.

---

## **Installation**

Install the package from GitHub (or PyPI if published):

```bash
pip install git+https://github.com/dhruvsyos/llmworkbook.git
```

---

## **Quick Start**

### **1. Install Dependencies**
Ensure you have the following dependencies installed:
- `pandas`
- `aiohttp`
- (Optional) `openai` if you prefer using OpenAI's SDK instead of REST.

You can install these via:

```bash
pip install pandas aiohttp openai
```

### **2. Import the Package**

```python
import pandas as pd
from llmworkbook import LLMConfig, LLMRunner, LLMDataFrameIntegrator
```

### **3. Create a Sample DataFrame**

```python
data = {
    "id": [1, 2, 3],
    "prompt_text": [
        "Explain Newton's first law in simple terms.",
        "Write a short poem about the moon.",
        "Give me 3 tips for better time management."
    ]
}
df = pd.DataFrame(data)
```

### **4. Configure the LLM**

```python
config = LLMConfig(
    provider_name="openai",
    api_key="YOUR_API_KEY",  # Replace with your API key
    model_name="gpt-3.5-turbo",
    system_prompt="You are a helpful assistant.",
    temperature=0.7,
    max_tokens=1000
)
```

### **5. Create a Runner and Integrate**

```python
runner = LLMRunner(config)
integrator = LLMDataFrameIntegrator(runner=runner, df=df)
```

### **6. Add LLM Responses to DataFrame**

```python
updated_df = integrator.add_llm_responses(
    prompt_column="prompt_text",
    response_column="llm_response",
    async_mode=False  # Set to True for asynchronous requests
)

print(updated_df)
```

Expected Output:

| id | prompt_text                                 | llm_response                                      |
|----|--------------------------------------------|--------------------------------------------------|
| 1  | Explain Newton's first law in simple terms.| An object at rest stays at rest unless acted on. |
| 2  | Write a short poem about the moon.         | The moon glows bright in the midnight light.     |
| 3  | Give me 3 tips for better time management. | 1. Plan ahead 2. Use tools 3. Take breaks.       |

---

## **Usage Documentation**

### **`LLMConfig`**

The `LLMConfig` class allows you to configure your LLM provider and relevant settings.

**Constructor Parameters:**
- `provider_name` (str): Name of the LLM provider (e.g., `openai`, `azure_openai`, etc.).
- `api_key` (str): API key for the provider.
- `model_name` (str, optional): Model name (e.g., `gpt-3.5-turbo`).
- `system_prompt` (str, optional): System-level prompt to guide LLM behavior.
- `temperature` (float): Controls randomness. Default is `0.7`.
- `max_tokens` (int): Maximum token count for responses. Default is `1024`.
- `additional_params` (dict, optional): Extra parameters for provider-specific configurations.

**Example:**

```python
config = LLMConfig(
    provider_name="openai",
    api_key="YOUR_API_KEY",
    model_name="gpt-3.5-turbo",
    system_prompt="You are a helpful assistant.",
    temperature=0.5,
    max_tokens=1500
)
```

---

### **`LLMRunner`**

Handles LLM calls and supports both synchronous and asynchronous modes.

**Methods:**
1. **`run(prompt: str) -> str`**: Async method to send a prompt and get a response.
2. **`run_sync(prompt: str) -> str`**: Synchronous wrapper for simpler usage.

**Example:**

```python
runner = LLMRunner(config)
response = runner.run_sync("What is the capital of France?")
print(response)  # Output: "Paris"
```

---

### **`LLMDataFrameIntegrator`**

Integrates LLM calls with a pandas DataFrame.

**Constructor Parameters:**
- `runner` (`LLMRunner`): LLM runner instance for handling API calls.
- `df` (`pandas.DataFrame`): DataFrame to which responses will be added.

**Methods:**
1. **`add_llm_responses(prompt_column: str, response_column: str = "llm_response", row_filter: Optional[List[int]] = None, async_mode: bool = False) -> pd.DataFrame`**

   **Parameters:**
   - `prompt_column` (str): Name of the column containing prompts.
   - `response_column` (str, optional): Name of the column to store responses. Default: `"llm_response"`.
   - `row_filter` (List[int], optional): List of row indices to process. Default: all rows.
   - `async_mode` (bool): If `True`, runs asynchronously. Default: `False`.

   **Returns:**
   - A DataFrame with the LLM responses added to the specified column.

**Example:**

```python
updated_df = integrator.add_llm_responses(
    prompt_column="prompt_text",
    response_column="llm_response",
    async_mode=True
)
```

---

## **Advanced Topics**

### **Async vs. Sync Modes**

- **Synchronous Mode**:
   ```python
   integrator.add_llm_responses(async_mode=False)
   ```
   Use this for simple use cases where performance isn't critical.

- **Asynchronous Mode**:
   ```python
   integrator.add_llm_responses(async_mode=True)
   ```
   Enables parallel processing of multiple rows, reducing latency for larger DataFrames.

---

### **Adding More Providers**

To add support for new providers (e.g., Cohere or Anthropic):
1. Implement a `_call_llm_<provider_name>()` method in `LLMRunner`.
2. Update the `run()` method to conditionally call the new provider's function.

---

## **Future Roadmap**

- Add support for more LLM providers (Azure OpenAI, Cohere, etc.).
- Implement rate-limiting and token usage tracking.
- Add streaming response handling.
- Publish as a PyPI package for easy installation.

---

## **Contributing**

We welcome contributions to this package! To contribute:
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-name`).
3. Commit your changes and submit a pull request.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Acknowledgments**

- **OpenAI**: For the powerful GPT models.
- **pandas**: For making DataFrame operations seamless.

---

This `README.md` provides a comprehensive guide to using the **LLMWorkbook** package, including installation, configuration, examples, and advanced usage documentation. You can adjust this further based on your specific package name and usage.
