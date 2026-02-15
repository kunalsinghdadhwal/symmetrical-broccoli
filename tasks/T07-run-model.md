# T7: run_model Agent

**Worktree:** `../t7-run-model`
**Branch:** `task/t7-run-model`
**Files created:** `src/agents/run_model.py`, `tests/unit/test_run_model.py`
**Depends on:** T2, T3
**Blocks:** T12, T15

---

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. Your job is to implement
ONLY the run_model agent. Other developers are building other modules in
parallel. Do not create or modify any files outside your scope.

This agent runs test prompts against the TARGET LLM (the model being evaluated
for hallucinations). It supports two providers: Bedrock (production) and Ollama
(testing). Ollama is NOT part of the production architecture -- it simulates a
hallucination-prone model during development.

DEPENDENCIES YOU CONSUME (do not implement, just import):
  from src.wrappers.bedrock import call_llm
  # call_llm(prompt: str, system: str = "") -> str

  from ollama import Client as OllamaClient
  # OllamaClient(host=str)
  # client.chat(model=str, messages=list[dict]) -> response
  # response.message.content -> str

INTERFACE YOU PRODUCE:
  File: src/agents/run_model.py

  Function: run_model(state: dict) -> None
    Reads:
      state["prompts"] (list[str])
      state["config"]["model"]["provider"] (str: "bedrock" or "ollama")
      state["config"]["model"]["model_id"] (str)

    Behavior:
      - For each prompt in state["prompts"]:
        - Calls call_target_llm(prompt, state["config"]["model"])
        - Appends {"prompt": prompt, "response": result} to responses list

    Writes:
      state["responses"] = list[dict]
        # [{"prompt": str, "response": str}, ...]

  Helper: call_target_llm(prompt: str, model_config: dict) -> str
    - If provider == "bedrock": return call_llm(prompt)
    - If provider == "ollama":
        client = OllamaClient(host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))
        response = client.chat(model=model_config["model_id"],
                               messages=[{"role": "user", "content": prompt}])
        return response.message.content
    - If provider is unknown: raise ValueError(f"Unknown provider: {provider}")

ALSO CREATE:
  File: tests/unit/test_run_model.py
    Mock both call_llm and OllamaClient.

    Test cases:
    - Bedrock provider: calls call_llm for each prompt
    - Ollama provider: creates OllamaClient, calls chat
    - Unknown provider raises ValueError
    - Number of responses equals number of prompts
    - Each response dict has "prompt" and "response" keys
    - Empty prompts list produces empty responses list

ACCEPTANCE CRITERIA:
  - pytest tests/unit/test_run_model.py passes
  - Imports from src/: only from src.wrappers.bedrock import call_llm
  - ollama import is at function level (not module level) so it does not
    break when ollama is not installed in production
  - Function signature is exactly: run_model(state: dict) -> None

Commit message: "feat: run_model agent with bedrock and ollama providers"
```
