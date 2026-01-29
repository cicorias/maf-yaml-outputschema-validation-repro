# Microsoft Agent Framework - outputSchema YAML Reproduction

This repository reproduces issues with the **Microsoft Agent Framework** when using `outputSchema` in declarative YAML agent definitions.

## Issue Summary

As of the current release (`agent-framework-*>=1.0.0b260128`), the `outputSchema` property defined in YAML agent specifications does not properly enforce structured output validation. When using `try_parse_value()` on agent responses, parsing fails even though the schema is correctly defined in the YAML.

## Environment

- **Python**: 3.12+
- **Agent Framework Packages** (as of January 2026):
  - `agent-framework-core>=1.0.0b260128`
  - `agent-framework-azure-ai>=1.0.0b260128`
  - `agent-framework-devui>=1.0.0b260128`
  - `agent-framework-declarative>=1.0.0b260128`

## Reproduction Steps

### 1. Setup

```bash
# Clone the repository
git clone <repo-url>
cd maf-yaml-outputschema-validation-repro

# Create virtual environment with uv
uv sync
```

### 2. Configure Environment Variables

Create a `.env` file with your Azure credentials:

```env
# For Azure OpenAI Responses API
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-key>

# For Azure AI Foundry
AZURE_AI_PROJECT_ENDPOINT=https://<your-project>.services.ai.azure.com/
```

### 3. Run Test Scripts

**Azure OpenAI Responses API:**

```bash
uv run python main_azure_openai_yaml.py
```

**Azure AI Foundry:**

```bash
uv run python main_foundry_yaml.py
```

**Direct YAML Test:**

```bash
uv run python main_yaml_file.py
```

## Expected Behavior

When `outputSchema` is defined in the YAML, the agent should:

1. Send the schema to the model as a `response_format` parameter
2. Return structured output matching the schema
3. Successfully parse via `response.try_parse_value()`

## Actual Behavior

- The `outputSchema` in YAML is loaded but not properly converted to a `response_format` parameter
- `try_parse_value()` returns `None` (parsing fails)
- The agent returns unstructured text instead of validated JSON

## YAML Examples

### Azure OpenAI Responses API ([AzureOpenAIResponses.yaml](yaml/AzureOpenAIResponses.yaml))

```yaml
kind: Prompt
name: Assistant
description: Helpful assistant
instructions: You are a helpful assistant...
model:
    id: gpt-4.1
    provider: AzureOpenAI
    apiType: Responses
    options:
        temperature: 0.9
        topP: 0.95
outputSchema:
    properties:
        language:
            type: string
            required: true
            description: The language of the answer.
        answer:
            type: string
            required: true
            description: The answer text.
```

### Azure AI Foundry ([AzureFoundryResponses.yaml](yaml/AzureFoundryResponses.yaml))

```yaml
kind: Prompt
name: Assistant
description: Helpful assistant
instructions: You are a helpful assistant...
model:
    id: gpt-4.1
    options:
        temperature: 0.9
        topP: 0.95
    connection:
        kind: Remote
        endpoint: =Env.AZURE_AI_PROJECT_ENDPOINT
outputSchema:
    properties:
        language:
            type: string
            required: true
            description: The language of the answer.
        answer:
            type: string
            required: true
            description: The answer text.
```

## Project Structure

```text
├── main_azure_openai_yaml.py   # Test with Azure OpenAI Responses API
├── main_foundry_yaml.py        # Test with Azure AI Foundry
├── main_yaml_file.py           # Direct YAML parsing test
├── pyproject.toml              # Dependencies
├── yaml/
│   ├── AzureOpenAIResponses.yaml
│   └── AzureFoundryResponses.yaml
└── cases/                      # Additional test cases (if any)
```

## Related Resources

- [Microsoft Agent Framework Documentation](https://github.com/microsoft/agent-framework)
- [Azure OpenAI Structured Outputs](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/structured-outputs)

## License

This reproduction repository is provided for issue demonstration purposes.
