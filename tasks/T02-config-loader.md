# T2: Config Loader

**Worktree:** `../t2-config-loader`
**Branch:** `task/t2-config-loader`
**Files created:** `src/config/loader.py`, `tests/unit/test_config_loader.py`, `.llm-reliability.yaml`
**Depends on:** T1
**Blocks:** T7, T13

---

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. Your job is to implement
ONLY the config loader module. Other developers are building other modules in
parallel. Do not create or modify any files outside your scope.

The config file (.llm-reliability.yaml) defines an organization's LLM evaluation
parameters. Your loader reads it, validates required fields, and returns a dict.

INTERFACE YOU PRODUCE:
  File: src/config/loader.py
  Function: load_config(path: str | None = None) -> dict
    - If path is None, defaults to ".llm-reliability.yaml" in cwd
    - Parses YAML
    - Validates required fields (raises ValueError with field name if missing):
        use_case                          (str)
        risk_tolerance.deploy_threshold   (float)
        risk_tolerance.warn_threshold     (float)
        doc_sources                       (list)
        model.provider                    (str)
        model.model_id                    (str)
        elasticsearch.host               (str)
        elasticsearch.index              (str)
    - Returns normalized dict with this shape:
        {
          "use_case": str,
          "thresholds": {"deploy": float, "warn": float},
          "evaluation": {"num_prompts": int, "prompt_categories": list[str]},
          "model": {"provider": str, "model_id": str},
          "elasticsearch": {"host": str, "index": str},
          "doc_sources": list[dict],
        }
      Note: "thresholds" is flattened from "risk_tolerance" for downstream use.
    - Raises FileNotFoundError for missing file path

ALSO CREATE:
  File: .llm-reliability.yaml (sample config in repo root)
    use_case: "customer support chatbot for Acme Corp"
    risk_tolerance:
      deploy_threshold: 0.10
      warn_threshold: 0.25
    evaluation:
      num_prompts: 20
      prompt_categories: [factual_recall, edge_cases, policy_boundaries, ambiguous_queries]
    doc_sources:
      - type: local
        path: ./docs/policies/
    model:
      provider: bedrock
      model_id: "anthropic.claude-3-sonnet-20240229-v1:0"
    elasticsearch:
      host: "http://localhost:9200"
      index: "trusted_docs"

  File: tests/unit/test_config_loader.py
    Test cases:
    - Valid YAML returns correct dict structure with flattened thresholds
    - Missing "use_case" raises ValueError mentioning "use_case"
    - Missing nested field "risk_tolerance.deploy_threshold" raises ValueError
    - Non-existent file path raises FileNotFoundError
    - None path defaults to .llm-reliability.yaml
    - Extra fields in YAML are preserved (not stripped)

ACCEPTANCE CRITERIA:
  - pytest tests/unit/test_config_loader.py passes
  - No imports from any other src/ module (this module has zero internal dependencies)

Commit message: "feat: config loader with YAML validation"
```
