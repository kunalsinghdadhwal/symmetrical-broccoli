# T4: Elasticsearch Helper

**Worktree:** `../t4-es-helper`
**Branch:** `task/t4-es-helper`
**Files created:** `src/wrappers/elasticsearch_helper.py`, `tests/unit/test_elasticsearch_helper.py`
**Depends on:** T1
**Blocks:** T9, T11, T15

---

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. Your job is to implement
ONLY the Elasticsearch helper module. Other developers are building other modules
in parallel. Do not create or modify any files outside your scope.

This module is the single interface to Elasticsearch. Three functions: index,
keyword search, vector search.

DEPENDENCY YOU CONSUME (do not implement, just import):
  from src.wrappers.bedrock import embed
  # embed(text: str) -> list[float]
  # You call this inside vector_search to get the query embedding.
  # In your tests, mock this function.

INTERFACE YOU PRODUCE:
  File: src/wrappers/elasticsearch_helper.py

  Module-level client:
    - from elasticsearch import Elasticsearch
    - Connection params from env vars:
        ES_HOST (default "http://localhost:9200")
        ES_API_KEY (optional, omit if empty)
    - Initialized once at module level

  Function: index_doc(index: str, doc_id: str, body: dict) -> None
    - Calls es.index(index=index, id=doc_id, document=body)

  Function: search_docs(query: str, index: str = "trusted_docs") -> list[dict]
    - BM25 keyword search: {"query": {"match": {"content": query}}}
    - Returns [hit["_source"] for hit in response["hits"]["hits"]]

  Function: vector_search(text: str, index: str = "trusted_docs", k: int = 5) -> list[dict]
    - Calls embed(text) to get query vector
    - kNN search using the search API knn parameter:
        knn={"field": "embedding", "query_vector": vector, "k": k, "num_candidates": 100}
    - Returns [hit["_source"] for hit in response["hits"]["hits"]]

ALSO CREATE:
  File: tests/unit/test_elasticsearch_helper.py
    Mock both the Elasticsearch client AND the embed function.

    Test cases:
    - index_doc calls es.index with correct params
    - search_docs returns _source from hits
    - search_docs uses match query on "content" field
    - vector_search calls embed() with the input text
    - vector_search passes embedding to knn search
    - vector_search returns _source from hits
    - Empty search results return empty list (not error)
    - ES client initialized once at module level

    Mock structures:
    es.search response:
      {"hits": {"hits": [
        {"_source": {"content": "doc text", "embedding": [0.1, 0.2]}, "_id": "1"},
        {"_source": {"content": "other doc", "embedding": [0.3, 0.4]}, "_id": "2"},
      ]}}

ACCEPTANCE CRITERIA:
  - pytest tests/unit/test_elasticsearch_helper.py passes
  - Only import from src/ is: from src.wrappers.bedrock import embed
  - grep confirms: no hardcoded ES host or index name in function bodies

Commit message: "feat: elasticsearch helper with keyword and vector search"
```
