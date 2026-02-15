# T12: Workflow Orchestrator

**Branch:** `task/t12-orchestrator` (from `main` after merging T2-T11)
**Files created:** `src/orchestrator.py`, `tests/unit/test_orchestrator.py`
**Depends on:** T5, T6, T7, T8, T9, T10
**Blocks:** T13

---

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. All agents have been
implemented by other developers and merged. Your job is to implement the
orchestrator that wires them into a sequential pipeline.

DEPENDENCIES YOU CONSUME (all exist, just import):
  from src.agents.generate_prompts import generate_prompts
  from src.agents.run_model import run_model
  from src.agents.extract_claims import extract_claims
  from src.agents.retrieve_evidence import retrieve_evidence
  from src.agents.verify_claims import verify_claims
  from src.agents.score_risk import score_risk

  Each has signature: fn(state: dict) -> None
  Each reads from and writes to the shared state dict.

INTERFACE YOU PRODUCE:
  File: src/orchestrator.py

  Function: run_workflow(state: dict) -> None
    - agents = [generate_prompts, run_model, extract_claims,
                retrieve_evidence, verify_claims, score_risk]
    - For each agent:
      - Log: "Starting {agent.__name__}"
      - Call agent(state)
      - Log: "Completed {agent.__name__}"
    - If an agent raises, log "Failed in {agent.__name__}: {error}" and re-raise
    - Use Python's logging module (logger = logging.getLogger(__name__))

  Function: build_response(state: dict) -> dict
    - Returns:
      {
        "score": state["score"]["risk"],
        "decision": state["score"]["decision"],
        "total_claims": state["score"]["total_claims"],
        "supported": state["score"]["supported"],
        "unsupported": state["score"]["unsupported"],
        "weakly_supported": state["score"]["weakly_supported"],
        "details": state.get("verdicts", []),
      }

ALSO CREATE:
  File: tests/unit/test_orchestrator.py
    Mock all six agent functions.

    Test cases:
    - All agents called in correct order
    - State dict is passed to each agent
    - Exception in agent 3 prevents agents 4-6 from running
    - build_response extracts correct fields from state
    - build_response handles missing verdicts key gracefully

ACCEPTANCE CRITERIA:
  - pytest tests/unit/test_orchestrator.py passes
  - Agents are called in exact pipeline order
  - Logging output is verifiable

Commit message: "feat: workflow orchestrator with sequential agent execution"
```
