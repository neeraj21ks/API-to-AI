from datetime import datetime, timedelta, timezone

from nexus.agents.manager import AgentManager
from nexus.contracts import BatchSnapshot
from nexus.detection.rules import detect_incidents


def test_agent_manager_returns_evidence_backed_non_executable_plan():
    now = datetime.now(timezone.utc)
    snapshot = BatchSnapshot(
        pipeline="demo",
        batch_id="batch-xyz",
        status="FAILED",
        started_at=now - timedelta(minutes=1),
        completed_at=now,
        records_extracted=10,
        records_loaded=0,
        records_quarantined=0,
        expected_records=10,
        error_message="source timeout",
    )
    incident = detect_incidents(snapshot)[0]
    report = AgentManager().investigate(incident, snapshot)

    assert [finding.agent for finding in report.findings] == [
        "triage", "investigation", "root_cause_analysis"
    ]
    assert report.recovery_plan.requires_human_approval is True
    assert report.recovery_plan.executable is False
    assert report.incident.evidence[0].evidence_id in report.findings[0].evidence_ids
    assert len(report.verification_checks) >= 4


def test_manager_rejects_mismatched_batch():
    now = datetime.now(timezone.utc)
    snapshot = BatchSnapshot(
        pipeline="demo",
        batch_id="batch-a",
        status="FAILED",
        started_at=now,
    )
    incident = detect_incidents(snapshot)[0]
    wrong_snapshot = BatchSnapshot(
        pipeline="demo",
        batch_id="batch-b",
        status="FAILED",
        started_at=now,
    )
    try:
        AgentManager().investigate(incident, wrong_snapshot)
    except ValueError as exc:
        assert "same batch" in str(exc)
    else:
        raise AssertionError("Expected batch mismatch to be rejected")
