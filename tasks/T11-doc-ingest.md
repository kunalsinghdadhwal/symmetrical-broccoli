# T11: Documentation Ingest Pipeline

**Worktree:** `../t11-doc-ingest`
**Branch:** `task/t11-doc-ingest`
**Files created:** `src/ingest/pipeline.py`, `tests/unit/test_ingest_pipeline.py`
**Depends on:** T3, T4
**Blocks:** T16

---

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. Your job is to implement
ONLY the documentation ingest pipeline. Other developers are building other
modules in parallel. Do not create or modify any files outside your scope.

This is an offline batch process. It reads trusted documents, cleans them, chunks
them, embeds each chunk, and indexes them into Elasticsearch. It runs BEFORE any
evaluation -- it populates the evidence base.

DEPENDENCIES YOU CONSUME (do not implement, just import):
  from src.config.loader import load_config
  # load_config(path: str | None = None) -> dict

  from src.wrappers.bedrock import embed
  # embed(text: str) -> list[float]

  from src.wrappers.elasticsearch_helper import index_doc
  # index_doc(index: str, doc_id: str, body: dict) -> None

INTERFACE YOU PRODUCE:
  File: src/ingest/pipeline.py

  Function: run_ingest(config_path: str) -> dict
    - Calls load_config(config_path)
    - Reads config["doc_sources"] and config["elasticsearch"]["index"]
    - For each source:
      - If type == "local": reads all files from source["path"]
        (recursively, .txt and .md files)
      - (type == "s3" can be stubbed with raise NotImplementedError for now)
    - For each file:
      - raw = read file contents
      - cleaned = clean_text(raw)
      - chunks = chunk_text(cleaned)
      - For each chunk:
        - vector = embed(chunk)
        - doc_id = hash of chunk content (use hashlib.sha256)
        - index_doc(index, doc_id, {"content": chunk, "embedding": vector})
    - Returns {"documents_processed": int, "chunks_indexed": int}

  Helper: clean_text(raw: str) -> str
    - Strip HTML tags (use re.sub or html parser)
    - Normalize whitespace (collapse multiple spaces/newlines to single space)
    - Strip leading/trailing whitespace

  Helper: chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]
    - Split text into words
    - Create chunks of chunk_size words with overlap words shared between
      consecutive chunks
    - Last chunk may be smaller than chunk_size
    - Single chunk if text is shorter than chunk_size

  CLI entry point: if __name__ == "__main__" block
    - Parse --config argument (default ".llm-reliability.yaml")
    - Call run_ingest(config_path)
    - Print summary

ALSO CREATE:
  File: tests/unit/test_ingest_pipeline.py
    Mock embed and index_doc. Use tmp_path fixture for local files.

    Test cases:
    - clean_text strips HTML tags
    - clean_text normalizes whitespace
    - chunk_text splits correctly with overlap
    - chunk_text handles text shorter than chunk_size (single chunk)
    - chunk_text overlap: last N words of chunk K == first N words of chunk K+1
    - run_ingest reads local files and indexes chunks
    - run_ingest returns accurate counts
    - Missing source path raises clear error
    - S3 source type raises NotImplementedError

ACCEPTANCE CRITERIA:
  - pytest tests/unit/test_ingest_pipeline.py passes
  - Imports from src/: load_config, embed, index_doc only
  - python -m src.ingest.pipeline --help works (does not crash)

Commit message: "feat: doc ingest pipeline with chunking and embedding"
```
