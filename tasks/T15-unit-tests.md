# T15: Unit Tests (catch-up)

**Branch:** `task/t15-unit-tests` (from `main` after merging all modules)
**Purpose:** Fill gaps in test coverage after merge
**Depends on:** T3, T4, T5, T6, T7, T8, T9, T10
**Blocks:** nothing

---

Each module task (T2-T11) already includes its own test file. This task covers cross-module tests and any gaps found after merge.

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. All modules have been
implemented and merged. Your job is to review existing test coverage and fill
any gaps.

INSTRUCTIONS:
1. Run `pytest tests/unit/ -v` and verify all existing tests pass.
2. Run `pytest tests/unit/ --co -q` to list all collected tests.
3. Check coverage gaps by reviewing each module in src/ against its test file.
4. Add missing tests for edge cases, error paths, or untested branches.

EXPECTED TEST FILES (already exist from individual tasks):
  tests/unit/test_config_loader.py
  tests/unit/test_bedrock_wrapper.py
  tests/unit/test_elasticsearch_helper.py
  tests/unit/test_score_risk.py
  tests/unit/test_generate_prompts.py
  tests/unit/test_run_model.py
  tests/unit/test_extract_claims.py
  tests/unit/test_retrieve_evidence.py
  tests/unit/test_verify_claims.py
  tests/unit/test_orchestrator.py
  tests/unit/test_api.py
  tests/unit/test_ingest_pipeline.py

ACCEPTANCE CRITERIA:
  - pytest tests/unit/ passes with zero failures
  - No test requires live AWS credentials, live Elasticsearch, or live Ollama

Skip this task if all individual task tests already pass and coverage is adequate.

Commit message: "test: fill unit test coverage gaps"
```
