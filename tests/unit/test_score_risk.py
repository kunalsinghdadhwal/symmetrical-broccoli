"""Tests for score_risk agent."""

from src.agents.score_risk import score_risk


def _make_state(labels, deploy=0.10, warn=0.25):
    """Build a minimal state dict for testing."""
    return {
        "verdicts": [{"label": l} for l in labels],
        "config": {"thresholds": {"deploy": deploy, "warn": warn}},
    }


class TestScoreRisk:
    def test_all_supported(self):
        state = _make_state(["supported", "supported", "supported"])
        score_risk(state)
        assert state["score"]["risk"] == 0.0
        assert state["score"]["decision"] == "deploy"

    def test_all_unsupported(self):
        state = _make_state(["unsupported", "unsupported", "unsupported"])
        score_risk(state)
        assert state["score"]["risk"] == 1.0
        assert state["score"]["decision"] == "block"

    def test_all_weakly_supported(self):
        state = _make_state(
            ["weakly_supported"] * 4, deploy=0.10, warn=0.25
        )
        score_risk(state)
        assert state["score"]["risk"] == 0.5
        assert state["score"]["decision"] == "block"

    def test_mixed_verdicts(self):
        labels = ["unsupported", "weakly_supported", "supported", "supported"]
        state = _make_state(labels)
        score_risk(state)
        assert state["score"]["risk"] == 0.375
        assert state["score"]["decision"] == "block"

    def test_empty_verdicts(self):
        state = _make_state([])
        score_risk(state)
        assert state["score"]["risk"] == 0.0
        assert state["score"]["decision"] == "deploy"

    def test_boundary_equals_deploy_threshold(self):
        # risk = 0.10 exactly should be "deploy"
        # 1 weakly out of 5 => risk = 0.5/5 = 0.10
        labels = ["weakly_supported"] + ["supported"] * 4
        state = _make_state(labels, deploy=0.10, warn=0.25)
        score_risk(state)
        assert state["score"]["risk"] == 0.1
        assert state["score"]["decision"] == "deploy"

    def test_boundary_equals_warn_threshold(self):
        # risk = 0.25 exactly should be "warn"
        # 1 weakly out of 2 => risk = 0.5/2 = 0.25
        labels = ["weakly_supported", "supported"]
        state = _make_state(labels, deploy=0.10, warn=0.25)
        score_risk(state)
        assert state["score"]["risk"] == 0.25
        assert state["score"]["decision"] == "warn"

    def test_score_has_all_keys(self):
        state = _make_state(["supported", "unsupported"])
        score_risk(state)
        expected_keys = {
            "risk", "decision", "total_claims",
            "supported", "weakly_supported", "unsupported",
        }
        assert set(state["score"].keys()) == expected_keys
