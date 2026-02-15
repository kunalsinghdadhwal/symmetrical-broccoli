# T6: generate_prompts Agent

**Worktree:** `../t6-gen-prompts`
**Branch:** `task/t6-gen-prompts`
**Files created:** `src/agents/generate_prompts.py`, `tests/unit/test_generate_prompts.py`
**Depends on:** T3
**Blocks:** T12, T15

---

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. Your job is to implement
ONLY the generate_prompts agent. Other developers are building other modules in
parallel. Do not create or modify any files outside your scope.

This agent reads the config to understand the use case, then asks Claude to
generate domain-specific test prompts that are likely to surface hallucinations.

DEPENDENCY YOU CONSUME (do not implement, just import):
  from src.wrappers.bedrock import call_llm
  # call_llm(prompt: str, system: str = "") -> str
  # In your tests, mock this function.

INTERFACE YOU PRODUCE:
  File: src/agents/generate_prompts.py

  Function: generate_prompts(state: dict) -> None
    Reads:
      state["config"]["use_case"] (str)
      state["config"]["evaluation"]["num_prompts"] (int)
      state["config"]["evaluation"]["prompt_categories"] (list[str])

    Behavior:
      - Constructs a system prompt telling Claude to generate test prompts for
        the given use case, covering the specified categories
      - Calls call_llm(prompt, system=system_prompt)
      - Parses Claude's response into individual prompt strings
      - If Claude returns fewer prompts than requested, keeps what it returned
      - If Claude returns more, truncates to num_prompts

    Writes:
      state["prompts"] = list[str]  # each element is a test prompt string

  Helper: parse_prompts(response: str) -> list[str]
    - Handles numbered lists ("1. ...", "2. ...")
    - Handles bullet points ("- ..." or "* ...")
    - Handles plain newline-separated text
    - Strips numbering/bullets from the result
    - Filters out empty strings

ALSO CREATE:
  File: tests/unit/test_generate_prompts.py
    Mock call_llm to return controlled responses.

    Test cases:
    - Numbered list response is parsed into correct number of prompts
    - Bullet point response is parsed correctly
    - Prompts are stripped of numbering/bullets
    - num_prompts limit is respected (response has more, list is truncated)
    - Empty response produces empty list (not error)
    - call_llm is called exactly once
    - state["prompts"] is written as list[str]

    Mock response example:
    "1. What is your return policy for electronics?\n2. Can I return items after 30 days?\n3. Do you offer free shipping?"

ACCEPTANCE CRITERIA:
  - pytest tests/unit/test_generate_prompts.py passes
  - Only import from src/ is: from src.wrappers.bedrock import call_llm
  - Function signature is exactly: generate_prompts(state: dict) -> None

Commit message: "feat: generate_prompts agent with prompt parsing"
```
