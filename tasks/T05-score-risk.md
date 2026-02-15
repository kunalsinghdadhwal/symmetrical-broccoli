# T5: score_risk Agent

**Worktree:** `../t5-score-risk`
**Branch:** `task/t5-score-risk`
**Files created:** `src/agents/score_risk.py`, `tests/unit/test_score_risk.py`
**Depends on:** T1
**Blocks:** T12, T15

---

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. Your job is to implement
ONLY the score_risk agent. Other developers are building other modules in
parallel. Do not create or modify any files outside your scope.

This agent is pure computation. It reads verdict labels from the shared state,
computes a weighted risk score, and produces a deploy/warn/block decision.
It has ZERO external dependencies -- no LLM calls, no search, no imports from
other src/ modules.

INTERFACE YOU PRODUCE:
  File: src/agents/score_risk.py

  Function: score_risk(state: dict) -> None
    Reads:
      state["verdicts"] -- list of dicts, each with a "label" key
        label is one of: "supported", "weakly_supported", "unsupported"
      state["config"]["thresholds"] -- dict with "deploy" (float) and "warn" (float)

    Computes:
      total = len(verdicts)
      unsupported_count = count where label == "unsupported"
      weakly_count = count where label == "weakly_supported"
      supported_count = total - unsupported_count - weakly_count
      risk = (unsupported_count * 1.0 + weakly_count * 0.5) / total
      Edge case: if total == 0, risk = 0.0

    Decision:
      if risk <= thresholds["deploy"]: decision = "deploy"
      elif risk <= thresholds["warn"]: decision = "warn"
      else: decision = "block"

    Writes:
      state["score"] = {
        "risk": round(risk, 4),
        "decision": decision,
        "total_claims": total,
        "supported": supported_count,
        "weakly_supported": weakly_count,
        "unsupported": unsupported_count,
      }

ALSO CREATE:
  File: tests/unit/test_score_risk.py
    No mocks needed. Pure unit tests.

    Test cases (minimum):
    1. All supported (3 verdicts) -> risk 0.0, decision "deploy"
    2. All unsupported (3 verdicts) -> risk 1.0, decision "block"
    3. All weakly_supported (4 verdicts) -> risk 0.5, decision "block" (with thresholds 0.10/0.25)
    4. Mixed: 1 unsupported, 1 weakly, 2 supported -> risk 0.375, decision "block"
    5. Empty verdicts list -> risk 0.0, decision "deploy"
    6. Boundary: risk exactly equals deploy_threshold -> decision "deploy"
    7. Boundary: risk exactly equals warn_threshold -> decision "warn"
    8. Verify state["score"] has all 6 expected keys

    Use thresholds {"deploy": 0.10, "warn": 0.25} for all tests unless
    testing boundary behavior.

ACCEPTANCE CRITERIA:
  - pytest tests/unit/test_score_risk.py passes
  - Zero imports from any other module (no boto3, no elasticsearch, no other src/)
  - Function signature is exactly: score_risk(state: dict) -> None

Commit message: "feat: score_risk agent with weighted risk computation"
```
