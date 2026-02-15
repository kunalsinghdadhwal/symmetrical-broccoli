"""Integration tests for the full evaluation pipeline via API."""

import pytest
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.api import app
from tests.integration.conftest import requires_elasticsearch, requires_ollama


MOCK_CLAIMS_RESPONSE = (
    "1. Acme Corp allows returns within 30 days of purchase.\n"
    "2. Shipping is free for orders over $50.\n"
    "3. All electronics carry a 2-year warranty."
)

MOCK_VERIFY_SUPPORTED = "LABEL: supported\nJUSTIFICATION: Evidence confirms this."


@requires_elasticsearch
@requires_ollama
class TestFullPipeline:
    """End-to-end tests that mock only LLM calls (Bedrock), using real ES."""

    def _get_client(self):
        return TestClient(app)

    @patch("src.agents.verify_claims.call_llm", return_value=MOCK_VERIFY_SUPPORTED)
    @patch("src.agents.extract_claims.call_llm", return_value=MOCK_CLAIMS_RESPONSE)
    @patch("src.agents.generate_prompts.call_llm", return_value="1. What is the return policy?\n2. What is the shipping cost?\n3. What is the warranty?")
    def test_evaluate_returns_valid_response(self, mock_gen, mock_extract, mock_verify, ingest_fixtures):
        client = self._get_client()
        resp = client.post("/evaluate", json={"config_path": "tests/fixtures/test_config.yaml"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["decision"] in ("deploy", "warn", "block")
        assert body["total_claims"] > 0
        assert len(body["details"]) > 0

    @patch("src.agents.verify_claims.call_llm", return_value=MOCK_VERIFY_SUPPORTED)
    @patch("src.agents.extract_claims.call_llm", return_value=MOCK_CLAIMS_RESPONSE)
    @patch("src.agents.generate_prompts.call_llm", return_value="1. What is the return policy?")
    def test_score_is_valid_float(self, mock_gen, mock_extract, mock_verify, ingest_fixtures):
        client = self._get_client()
        resp = client.post("/evaluate", json={"config_path": "tests/fixtures/test_config.yaml"})
        body = resp.json()
        assert isinstance(body["score"], float)
        assert 0.0 <= body["score"] <= 1.0

    def test_health_endpoint(self):
        client = self._get_client()
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}
