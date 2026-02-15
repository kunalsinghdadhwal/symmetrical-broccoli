# T13: FastAPI Backend

**Branch:** `task/t13-fastapi` (from `main` after merging T12)
**Files created:** `src/api.py`, `tests/unit/test_api.py`
**Depends on:** T2, T12
**Blocks:** T14, T16

---

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. The config loader and
orchestrator have been implemented by other developers and merged. Your job is
to implement the FastAPI HTTP layer.

DEPENDENCIES YOU CONSUME (all exist, just import):
  from src.config.loader import load_config
  # load_config(path: str | None = None) -> dict

  from src.orchestrator import run_workflow, build_response
  # run_workflow(state: dict) -> None
  # build_response(state: dict) -> dict

INTERFACE YOU PRODUCE:
  File: src/api.py

  Pydantic models:
    class EvaluateRequest(BaseModel):
      config_path: str | None = None

    class EvaluateResponse(BaseModel):
      score: float
      decision: str
      total_claims: int
      supported: int
      unsupported: int
      weakly_supported: int
      details: list[dict]

  Endpoints:
    POST /evaluate
      - Accepts EvaluateRequest
      - Calls load_config(request.config_path)
      - state = {"config": config}
      - Calls run_workflow(state)
      - Returns EvaluateResponse from build_response(state)
      - On ValueError (bad config): return HTTP 400
      - On FileNotFoundError: return HTTP 404

    GET /health
      - Returns {"status": "ok"}

  App: app = FastAPI(title="LLM Reliability Gate")
  Entry: uvicorn src.api:app

ALSO CREATE:
  File: tests/unit/test_api.py
    Use httpx.AsyncClient with FastAPI TestClient. Mock load_config
    and run_workflow.

    Test cases:
    - POST /evaluate returns 200 with valid response schema
    - POST /evaluate with bad config returns 400
    - POST /evaluate with missing file returns 404
    - GET /health returns 200 with {"status": "ok"}
    - Response matches EvaluateResponse schema

ACCEPTANCE CRITERIA:
  - pytest tests/unit/test_api.py passes
  - uvicorn src.api:app starts without error (manual check)
  - /docs endpoint shows OpenAPI documentation

Commit message: "feat: fastapi backend with /evaluate and /health endpoints"
```
