# T3: Bedrock Wrapper

**Worktree:** `../t3-bedrock-wrapper`
**Branch:** `task/t3-bedrock-wrapper`
**Files created:** `src/wrappers/bedrock.py`, `tests/unit/test_bedrock_wrapper.py`
**Depends on:** T1
**Blocks:** T6, T7, T8, T9, T10, T11, T15

---

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. Your job is to implement
ONLY the AWS Bedrock wrapper module. Other developers are building other modules
in parallel. Do not create or modify any files outside your scope.

This wrapper is the single point of contact with AWS Bedrock. It exposes two
functions: one for LLM calls (Claude via Converse API) and one for embeddings
(Titan via invoke_model). All other modules import from here.

INTERFACE YOU PRODUCE:
  File: src/wrappers/bedrock.py

  Function: call_llm(prompt: str, system: str = "") -> str
    - Creates a bedrock-runtime client via boto3 (initialized once at module level)
    - Uses the Converse API (client.converse method), NOT invoke_model for this
    - Model ID from env var BEDROCK_MODEL_ID, default "anthropic.claude-3-sonnet-20240229-v1:0"
    - Region from env var AWS_DEFAULT_REGION, default "us-east-1"
    - Message format: [{"role": "user", "content": [{"text": prompt}]}]
    - System prompt format: [{"text": system}] if system is non-empty, else omit
    - Inference config: {"maxTokens": 4096, "temperature": 0.0}
    - Returns: response["output"]["message"]["content"][0]["text"]
    - No retries. No streaming. No caching.

  Function: embed(text: str) -> list[float]
    - Uses the same bedrock-runtime client
    - Calls client.invoke_model (NOT converse)
    - Model ID from env var TITAN_MODEL_ID, default "amazon.titan-embed-text-v2:0"
    - Request body: json.dumps({"inputText": text})
    - accept="application/json", contentType="application/json"
    - Returns: json.loads(response["body"].read())["embedding"]

DESIGN RULES (enforce these):
    - boto3.client initialized ONCE at module level, not per call
    - No retry logic anywhere
    - No streaming support
    - No response caching
    - Credentials come from environment (standard AWS credential chain)

ALSO CREATE:
  File: tests/unit/test_bedrock_wrapper.py
    All tests must mock boto3.client so they run without AWS credentials.

    Test cases:
    - call_llm returns text from mocked converse response
    - call_llm passes system prompt when provided
    - call_llm omits system prompt when empty string
    - call_llm uses temperature 0.0 and maxTokens 4096
    - embed returns list of floats from mocked invoke_model response
    - embed sends correct body format with inputText
    - Module-level client is created once (patch boto3.client, call both
      functions, assert boto3.client called once)

    Mock response structures:
    converse response:
      {"output": {"message": {"content": [{"text": "mocked response"}]}},
       "usage": {"inputTokens": 10, "outputTokens": 5, "totalTokens": 15},
       "stopReason": "end_turn"}

    invoke_model response:
      body must be a mock with .read() returning:
      json.dumps({"embedding": [0.1, 0.2, 0.3], "inputTextTokenCount": 3})

ACCEPTANCE CRITERIA:
  - pytest tests/unit/test_bedrock_wrapper.py passes
  - No imports from any other src/ module
  - grep confirms: no "retry", no "cache", no "stream" in the module

Commit message: "feat: bedrock wrapper with call_llm and embed"
```
