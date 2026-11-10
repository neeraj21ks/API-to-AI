from datetime import datetime, timedelta, timezone

from nexus.contracts import BatchSnapshot, Severity
from nexus.detection.rules import detect_incidents


def snapshot(**overrides):
    now = datetime.now(timezone.utc)
    values = dict(
        pipeline="test_pipeline",
        batch_id="batch-001",
        status="SUCCESS",
        started_at=now - timedelta(seconds=30),
        completed_at=now,
        records_extracted=100,
        records_loaded=100,
        records_quarantined=0,
        expected_records=100,
    )
    values.update(overrides)
    return BatchSnapshot(**values)


def test_successful_healthy_batch_has_no_incidents():
    assert detect_incidents(snapshot()) == []


def test_failed_batch_creates_high_severity_incident():
    incidents = detect_incidents(snapshot(status="FAILED", error_message="database unavailable"))
    assert len(incidents) == 1
    assert incidents[0].severity == Severity.HIGH
    assert incidents[0].evidence[0].kind == "PIPELINE_STATUS"


def test_success_with_zero_output_is_critical():
    incidents = detect_incidents(snapshot(records_extracted=0, records_loaded=0))
    assert any(item.severity == Severity.CRITICAL for item in incidents)


def test_quarantine_ratio_threshold_is_explainable():
    incidents = detect_incidents(snapshot(records_loaded=90, records_quarantined=10))
    quarantine = next(item for item in incidents if item.title.startswith("Data quality"))
    assert quarantine.evidence[0].details["quarantine_ratio"] == 0.1


def test_duration_threshold_detects_slow_batch():
    now = datetime.now(timezone.utc)
    slow = snapshot(started_at=now - timedelta(hours=1), completed_at=now)
    incidents = detect_incidents(slow, slow_run_seconds=60)
    assert any("duration" in item.title.lower() for item in incidents)
