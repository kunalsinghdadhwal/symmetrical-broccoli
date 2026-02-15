"""score_risk -- compute weighted risk score from claim verdicts."""


def score_risk(state: dict) -> None:
    """Read verdicts, compute risk score, write decision to state."""
    verdicts = state["verdicts"]
    thresholds = state["config"]["thresholds"]

    total = len(verdicts)

    if total == 0:
        risk = 0.0
        unsupported_count = 0
        weakly_count = 0
        supported_count = 0
    else:
        unsupported_count = sum(
            1 for v in verdicts if v["label"] == "unsupported"
        )
        weakly_count = sum(
            1 for v in verdicts if v["label"] == "weakly_supported"
        )
        supported_count = total - unsupported_count - weakly_count
        risk = (unsupported_count * 1.0 + weakly_count * 0.5) / total

    if risk <= thresholds["deploy"]:
        decision = "deploy"
    elif risk <= thresholds["warn"]:
        decision = "warn"
    else:
        decision = "block"

    state["score"] = {
        "risk": round(risk, 4),
        "decision": decision,
        "total_claims": total,
        "supported": supported_count,
        "weakly_supported": weakly_count,
        "unsupported": unsupported_count,
    }
