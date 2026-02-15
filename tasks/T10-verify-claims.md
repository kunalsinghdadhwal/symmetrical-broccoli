# T10: verify_claims Agent

**Worktree:** `../t10-verify-claims`
**Branch:** `task/t10-verify-claims`
**Files created:** `src/agents/verify_claims.py`, `tests/unit/test_verify_claims.py`
**Depends on:** T3
**Blocks:** T12, T15

---

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. Your job is to implement
ONLY the verify_claims agent. Other developers are building other modules in
parallel. Do not create or modify any files outside your scope.

This agent is the core verification step. For each claim + evidence pair, it asks
Claude whether the evidence supports the claim. It labels each claim as:
  - "supported" -- directly confirmed by evidence
  - "weakly_supported" -- partially confirmed or ambiguous evidence
  - "unsupported" -- no support or contradicted

CRITICAL DESIGN RULE: The verifier sees ONLY the claim text and evidence text.
No other context. This prevents the generation model from influencing verification.

DEPENDENCY YOU CONSUME (do not implement, just import):
  from src.wrappers.bedrock import call_llm
  # call_llm(prompt: str, system: str = "") -> str

INTERFACE YOU PRODUCE:
  File: src/agents/verify_claims.py

  Function: verify_claims(state: dict) -> None
    Reads:
      state["evidence"] -- list of {"claim": dict, "documents": list[dict]}
        where claim has "text" key
        where each document has "content" key

    Behavior:
      - For each evidence entry:
        - If documents list is empty: verdict is "unsupported" with
          justification "No evidence documents found."
        - Otherwise:
          - Constructs a prompt with the claim text and concatenated
            evidence document contents
          - System prompt instructs Claude to:
            * Compare the claim against the provided evidence ONLY
            * Respond with exactly one label: supported, weakly_supported, unsupported
            * Provide a one-sentence justification
            * Format: "LABEL: <label>\nJUSTIFICATION: <text>"
          - Calls call_llm(prompt, system=system_prompt)
          - Parses response to extract label and justification

    Writes:
      state["verdicts"] = list[dict]
        # [{"claim": str, "label": str, "justification": str}, ...]
        # label is ALWAYS one of: "supported", "weakly_supported", "unsupported"

  Helper: parse_verdict(response: str) -> tuple[str, str]
    - Extracts label and justification from Claude's response
    - If parsing fails, defaults to ("unsupported", "Could not parse verification response.")
    - Normalizes label to lowercase, strips whitespace

ALSO CREATE:
  File: tests/unit/test_verify_claims.py
    Mock call_llm.

    Test cases:
    - Supported claim returns correct label and justification
    - Unsupported claim returns correct label
    - Weakly supported claim returns correct label
    - Empty documents list -> "unsupported" without calling call_llm
    - Malformed LLM response defaults to "unsupported"
    - Label is always lowercase
    - One verdict per evidence entry
    - call_llm receives only claim text and evidence text (no other context)

    Mock response examples:
    "LABEL: supported\nJUSTIFICATION: The evidence directly confirms the 30-day return policy."
    "LABEL: unsupported\nJUSTIFICATION: No evidence mentions this pricing."

ACCEPTANCE CRITERIA:
  - pytest tests/unit/test_verify_claims.py passes
  - Only import from src/ is: from src.wrappers.bedrock import call_llm
  - Function signature is exactly: verify_claims(state: dict) -> None

Commit message: "feat: verify_claims agent with evidence-based labeling"
```
