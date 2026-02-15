# T8: extract_claims Agent

**Worktree:** `../t8-extract-claims`
**Branch:** `task/t8-extract-claims`
**Files created:** `src/agents/extract_claims.py`, `tests/unit/test_extract_claims.py`
**Depends on:** T3
**Blocks:** T12, T15

---

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. Your job is to implement
ONLY the extract_claims agent. Other developers are building other modules in
parallel. Do not create or modify any files outside your scope.

This agent takes LLM responses and decomposes them into atomic factual claims.
Example: "Our return policy allows returns within 30 days, and shipping is free
for orders over $50" becomes two claims:
  1. "The return policy allows returns within 30 days."
  2. "Shipping is free for orders over $50."

DEPENDENCY YOU CONSUME (do not implement, just import):
  from src.wrappers.bedrock import call_llm
  # call_llm(prompt: str, system: str = "") -> str

INTERFACE YOU PRODUCE:
  File: src/agents/extract_claims.py

  Function: extract_claims(state: dict) -> None
    Reads:
      state["responses"] -- list of {"prompt": str, "response": str}

    Behavior:
      - For each response entry:
        - Constructs a prompt asking Claude to extract atomic factual claims
        - The system prompt should instruct Claude to:
          * Extract ONLY factual claims (not opinions, hedges, meta-commentary)
          * Make each claim atomic (one fact per claim)
          * Return a numbered list
          * If no factual claims exist, return "NO CLAIMS"
        - Calls call_llm(prompt, system=system_prompt)
        - Parses response into claim strings
        - Creates claim dicts with traceability back to source

    Writes:
      state["claims"] = list[dict]
        # [{"text": str, "source_prompt": str, "source_response": str}, ...]

  Helper: parse_claims(response: str) -> list[str]
    - Parses numbered list into individual claim strings
    - Handles "NO CLAIMS" -> returns empty list
    - Strips numbering
    - Filters empty strings

ALSO CREATE:
  File: tests/unit/test_extract_claims.py
    Mock call_llm.

    Test cases:
    - Response with two facts produces two claim dicts
    - Each claim dict has "text", "source_prompt", "source_response"
    - "NO CLAIMS" response produces zero claims (not error)
    - call_llm is called once per response entry
    - Multiple responses accumulate claims into single flat list
    - parse_claims handles numbered lists correctly

    Mock response example:
    "1. The return policy allows returns within 30 days.\n2. Shipping is free for orders over $50."

ACCEPTANCE CRITERIA:
  - pytest tests/unit/test_extract_claims.py passes
  - Only import from src/ is: from src.wrappers.bedrock import call_llm
  - Function signature is exactly: extract_claims(state: dict) -> None

Commit message: "feat: extract_claims agent with atomic claim decomposition"
```
