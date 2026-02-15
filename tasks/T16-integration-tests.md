# T16: Integration Tests

**Branch:** `task/t16-integration-tests` (from `main` after merging T11 + T13)
**Files created:** `tests/integration/test_full_pipeline.py`, `tests/integration/test_ingest.py`, `tests/fixtures/*`, `docker-compose.test.yml`
**Depends on:** T11, T13
**Blocks:** nothing

---

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. All modules have been
implemented and merged. Your job is to write integration tests that validate
the full pipeline using Ollama (as a hallucination-prone target) and a local
Elasticsearch instance.

INSTRUCTIONS:

Create: tests/fixtures/trusted_docs/
  Add 2-3 small .txt files with known content, e.g.:
  - return_policy.txt: "Acme Corp allows returns within 30 days of purchase.
    Items must be in original packaging. Refunds are processed within 5
    business days."
  - shipping_policy.txt: "Standard shipping is free for orders over $50.
    Express shipping costs $9.99. International shipping is not available."

Create: tests/fixtures/test_config.yaml
  A .llm-reliability.yaml pointing to:
  - doc_sources: [{type: local, path: tests/fixtures/trusted_docs/}]
  - model: {provider: ollama, model_id: "llama3.2"}
  - elasticsearch: {host: "http://localhost:9200", index: "test_trusted_docs"}
  - risk_tolerance: {deploy_threshold: 0.10, warn_threshold: 0.25}
  - evaluation: {num_prompts: 5, prompt_categories: [factual_recall, edge_cases]}
  - use_case: "customer support chatbot for Acme Corp"

Create: docker-compose.test.yml
  Single Elasticsearch service:
  - image: docker.elastic.co/elasticsearch/elasticsearch:8.17.0
  - single-node discovery
  - security disabled (xpack.security.enabled=false)
  - port 9200

Create: tests/integration/test_ingest.py
  - Ingest the fixture docs into local ES
  - Verify search_docs returns results for "return policy"
  - Verify vector_search returns results for "refund items"

Create: tests/integration/test_full_pipeline.py
  - Ingest fixture docs first
  - POST /evaluate with the test config (use httpx test client)
  - Assert response has valid schema
  - Assert total_claims > 0
  - Assert decision is one of: deploy, warn, block
  - Assert details list is non-empty

ACCEPTANCE CRITERIA:
  - Tests pass with: docker compose -f docker-compose.test.yml up -d && pytest tests/integration/
  - Requires Ollama running locally with llama3.2 pulled
  - Tests are skipped (not failed) if ES or Ollama are unavailable

Commit message: "test: integration tests with ollama and local elasticsearch"
```
