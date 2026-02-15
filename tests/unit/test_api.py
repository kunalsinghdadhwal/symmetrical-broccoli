"""Tests for FastAPI backend."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)

MODULE = "src.api"

MOCK_SCORE = {
    "risk": 0.25,
    "decision": "warn",
    "total_claims": 10,
    "supported": 6,
    "unsupported": 2,
    "weakly_supported": 2,
}

MOCK_VERDICTS = [
    {"claim": "test claim", "label": "supported", "justification": "ok"},
]


def _setup_workflow_side_effect(state):
    """Mutate state dict as run_workflow would."""
    state["score"] = MOCK_SCORE
    state["verdicts"] = MOCK_VERDICTS


class TestEvaluate:
    @patch(f"{MODULE}.run_workflow", side_effect=_setup_workflow_side_effect)
    @patch(f"{MODULE}.load_config", return_value={"use_case": "test"})
    def test_returns_200_with_valid_response(self, mock_config, mock_workflow):
        resp = client.post("/evaluate", json={"config_path": "test.yaml"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["score"] == 0.25
        assert body["decision"] == "warn"

    @patch(f"{MODULE}.run_workflow", side_effect=_setup_workflow_side_effect)
    @patch(f"{MODULE}.load_config", return_value={"use_case": "test"})
    def test_response_has_all_expected_keys(self, mock_config, mock_workflow):
        resp = client.post("/evaluate", json={"config_path": "test.yaml"})
        body = resp.json()
        expected_keys = {
            "score",
            "decision",
            "total_claims",
            "supported",
            "unsupported",
            "weakly_supported",
            "details",
        }
        assert set(body.keys()) == expected_keys

    @patch(f"{MODULE}.load_config", side_effect=ValueError("bad config"))
    def test_bad_config_returns_400(self, mock_config):
        resp = client.post("/evaluate", json={"config_path": "bad.yaml"})
        assert resp.status_code == 400
        assert "bad config" in resp.json()["detail"]

    @patch(f"{MODULE}.load_config", side_effect=FileNotFoundError("not found"))
    def test_missing_config_returns_404(self, mock_config):
        resp = client.post("/evaluate", json={"config_path": "missing.yaml"})
        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"]

    @patch(f"{MODULE}.run_workflow", side_effect=_setup_workflow_side_effect)
    @patch(f"{MODULE}.load_config", return_value={"use_case": "test"})
    def test_config_path_passed_through(self, mock_config, mock_workflow):
        client.post("/evaluate", json={"config_path": "/my/config.yaml"})
        mock_config.assert_called_once_with("/my/config.yaml")

    @patch(f"{MODULE}.run_workflow", side_effect=_setup_workflow_side_effect)
    @patch(f"{MODULE}.load_config", return_value={"use_case": "test"})
    def test_none_config_path_with_empty_body(self, mock_config, mock_workflow):
        resp = client.post("/evaluate", json={})
        assert resp.status_code == 200
        mock_config.assert_called_once_with(None)


class TestHealth:
    def test_returns_200_ok(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}
