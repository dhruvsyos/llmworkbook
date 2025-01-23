# **LLMWorkbook**

> [!WARNING]
> This repo is in development and may not be secure. Use is at your own risk

**LLMWorkbook** is a Python package designed to seamlessly integrate Large Language Models (LLMs) into your workflow with DataFrames/Arrays. This package allows you to easily configure an LLM, send prompts **row-wise** from a DataFrame/Arrays, and store responses back in the DataFrame with minimal effort.

---

## **Features**

- Configure LLM providers (e.g., OpenAI) using a simple configuration object.
- Asynchronous and synchronous support for LLM calls.
- Easily map LLM responses to a specific column in a pandas DataFrame.
- Built-in wrapper utilities to prepare data for LLM consumption.
- Extendable architecture for multiple LLM providers.
- Built-in utilities for preprocessing and handling API limits.

---

## **Installation**

Install the package from GitHub:

```bash
    pip install git+https://github.com/dhruvsyos/llmworkbook.git
```

---

## **Quick Start**
Not updated regularly. Please check examples for more detailed code samples.

---

### **Wrapper Utilities for LLM Preparation**

`LLMWorkbook` provides wrapper utilities to prepare various data formats for LLM consumption. These utilities transform input data into a format suitable for LLM processing, ensuring consistency and compatibility.
These wrapper methods can handle popular data sources like Excel (xlsx), CSV, Pandas DataFrames, multi dimensional arrays.

*See Examples for details.*
---

### **1. Import the Package**

```python
import pandas as pd
from llmworkbook import LLMConfig, LLMRunner, LLMDataFrameIntegrator
```

### **2. DataFrame**

```python
# Provide a dataframe, the usual
df = pd.DataFrame(data)
```

### **3. Configure the LLM**

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

### **4. Create a Runner and Integrate**

```python
runner = LLMRunner(config)
integrator = LLMDataFrameIntegrator(runner=runner, df=df)
```

### **5. Add LLM Responses to DataFrame**

```python
updated_df = integrator.add_llm_responses(
    prompt_column="prompt_text",
    response_column="llm_response",
    async_mode=False  # Set to True for asynchronous requests
)

```

---

## **Future Roadmap**

- Add support for more LLM providers (Azure OpenAI, Cohere, etc.).
- Implement rate-limiting and token usage tracking.
- Add streaming response handling.
- Publish as a PyPI package for easy installation.
- Add CLI method for developers
- Add an interface frontend for low code applications
