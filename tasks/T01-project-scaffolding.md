# T1: Project Scaffolding

**Branch:** `main` (commit directly, all worktrees branch from this)
**Files created:** `pyproject.toml`, `Makefile`, `.env.example`, `.gitignore`, `src/**/__init__.py`, `tests/**/__init__.py`
**Depends on:** nothing
**Blocks:** all other tasks

---

## Agent Prompt

```
CONTEXT:
You are setting up a Python project called "llm-reliability-gate". This is the
first task -- nothing exists yet. Every subsequent task branches from your commit.

INSTRUCTIONS:
Create the following project structure. Do not implement any logic -- only create
the skeleton with empty __init__.py files, the build config, and dev tooling.

Directory structure:
  src/
    __init__.py
    config/
      __init__.py
    agents/
      __init__.py
    wrappers/
      __init__.py
    ingest/
      __init__.py
  tests/
    __init__.py
    unit/
      __init__.py
    integration/
      __init__.py
    fixtures/

pyproject.toml:
  - name: llm-reliability-gate
  - requires-python: ">=3.11"
  - dependencies: fastapi, uvicorn, pydantic, boto3, elasticsearch, pyyaml
  - optional dev dependencies: pytest, httpx, ollama
  - package source: src/

.env.example:
  AWS_ACCESS_KEY_ID=
  AWS_SECRET_ACCESS_KEY=
  AWS_DEFAULT_REGION=us-east-1
  BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
  TITAN_MODEL_ID=amazon.titan-embed-text-v2:0
  ES_HOST=http://localhost:9200
  ES_API_KEY=
  ES_INDEX=trusted_docs
  OLLAMA_HOST=http://localhost:11434

Makefile targets:
  dev    - pip install -e ".[dev]"
  test   - pytest tests/
  ingest - python -m src.ingest.pipeline

.gitignore:
  Standard Python gitignore + .env, __pycache__, *.egg-info, .venv/

ACCEPTANCE CRITERIA:
  - `pip install -e ".[dev]"` succeeds
  - `pytest` exits cleanly with 0 tests collected
  - all __init__.py files exist

Commit message: "scaffold: project structure, build config, dev tooling"
```
