# T14: GitHub Action

**Branch:** `task/t14-github-action` (from `main` after merging T13)
**Files created:** `.github/workflows/llm-reliability.yml`
**Depends on:** T13
**Blocks:** nothing

---

## Agent Prompt

```
CONTEXT:
You are working on the LLM Reliability Gate project. The FastAPI backend is
complete. Your job is to create a GitHub Action workflow that calls the
/evaluate endpoint and gates deployments based on the result.

INSTRUCTIONS:
Create: .github/workflows/llm-reliability.yml

  name: LLM Reliability Gate
  on:
    pull_request:
      branches: [main]
    workflow_dispatch:

  jobs:
    evaluate:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4

        - name: Set up Python
          uses: actions/setup-python@v5
          with:
            python-version: "3.11"

        - name: Install dependencies
          run: pip install -e .

        - name: Start server
          run: |
            uvicorn src.api:app --host 0.0.0.0 --port 8000 &
            sleep 5
          env:
            AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
            AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
            AWS_DEFAULT_REGION: ${{ secrets.AWS_DEFAULT_REGION }}
            ES_HOST: ${{ secrets.ES_HOST }}
            ES_API_KEY: ${{ secrets.ES_API_KEY }}

        - name: Run evaluation
          id: evaluate
          run: |
            RESPONSE=$(curl -s -X POST http://localhost:8000/evaluate \
              -H "Content-Type: application/json" \
              -d '{"config_path": ".llm-reliability.yaml"}')
            echo "response=$RESPONSE" >> $GITHUB_OUTPUT
            DECISION=$(echo "$RESPONSE" | jq -r '.decision')
            echo "decision=$DECISION" >> $GITHUB_OUTPUT

        - name: Gate deployment
          run: |
            DECISION="${{ steps.evaluate.outputs.decision }}"
            if [ "$DECISION" = "block" ]; then
              echo "::error::Hallucination risk too high. Deployment blocked."
              exit 1
            elif [ "$DECISION" = "warn" ]; then
              echo "::warning::Elevated hallucination risk. Review recommended."
            else
              echo "Hallucination risk acceptable. Safe to deploy."
            fi

ACCEPTANCE CRITERIA:
  - YAML is valid syntax
  - Secrets are referenced, never hardcoded
  - "block" -> exit 1 (CI fails)
  - "warn" -> warning annotation (CI passes)
  - "deploy" -> clean pass

Commit message: "ci: github action for hallucination gate"
```
