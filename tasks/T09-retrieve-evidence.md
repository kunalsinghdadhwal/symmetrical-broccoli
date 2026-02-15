# T9: retrieve_evidence Agent

**Worktree:** `../t9-retrieve-evidence`
**Branch:** `task/t9-retrieve-evidence`
**Files created:** `src/agents/retrieve_evidence.py`, `tests/unit/test_retrieve_evidence.py`
**Depends on:** T3, T4
**Blocks:** T12, T15

---

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. Your job is to implement
ONLY the retrieve_evidence agent. Other developers are building other modules in
parallel. Do not create or modify any files outside your scope.

This agent queries Elasticsearch for each claim, combining keyword search (BM25)
and vector search (kNN) to find relevant trusted documentation.

DEPENDENCIES YOU CONSUME (do not implement, just import):
  from src.wrappers.elasticsearch_helper import search_docs, vector_search
  # search_docs(query: str, index: str = "trusted_docs") -> list[dict]
  # vector_search(text: str, index: str = "trusted_docs", k: int = 5) -> list[dict]

INTERFACE YOU PRODUCE:
  File: src/agents/retrieve_evidence.py

  Function: retrieve_evidence(state: dict) -> None
    Reads:
      state["claims"] -- list of {"text": str, "source_prompt": str, "source_response": str}
      state["config"]["elasticsearch"]["index"] (str)

    Behavior:
      - For each claim:
        - keyword_results = search_docs(claim["text"], index=config_index)
        - vector_results = vector_search(claim["text"], index=config_index)
        - combined = deduplicate(keyword_results + vector_results)
        - Append {"claim": claim, "documents": combined}

    Writes:
      state["evidence"] = list[dict]
        # [{"claim": dict, "documents": list[dict]}, ...]

  Helper: deduplicate(results: list[dict]) -> list[dict]
    - Removes duplicates based on document "content" field
    - If "content" key missing, fall back to full dict equality
    - Preserves order (first occurrence wins)

ALSO CREATE:
  File: tests/unit/test_retrieve_evidence.py
    Mock search_docs and vector_search.

    Test cases:
    - Each claim produces one evidence entry
    - Keyword and vector results are combined
    - Duplicates (same "content" value) are removed
    - No results from either search -> documents is empty list
    - Index name comes from state config, not hardcoded
    - search_docs and vector_search each called once per claim

    Mock data:
    keyword returns: [{"content": "doc A"}, {"content": "doc B"}]
    vector returns:  [{"content": "doc B"}, {"content": "doc C"}]
    deduplicated:    [{"content": "doc A"}, {"content": "doc B"}, {"content": "doc C"}]

ACCEPTANCE CRITERIA:
  - pytest tests/unit/test_retrieve_evidence.py passes
  - Only imports from src/: from src.wrappers.elasticsearch_helper import search_docs, vector_search
  - Function signature is exactly: retrieve_evidence(state: dict) -> None

Commit message: "feat: retrieve_evidence agent with dual search and dedup"
```
