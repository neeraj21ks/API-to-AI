"""First-pass, explainable pipeline incident detection."""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from nexus.contracts import (
    BatchSnapshot, Evidence, Incident, IncidentStatus, Severity, new_evidence,
)


def detect_incidents(
    snapshot: BatchSnapshot,
    *,
    quarantine_ratio_threshold: float = 0.05,
    slow_run_seconds: float = 900.0,
) -> list[Incident]:
    """Evaluate a batch snapshot and emit zero or more evidence-backed incidents.

    Rules are deliberately deterministic. No LLM decides whether an incident exists.
    """
    if not 0 <= quarantine_ratio_threshold <= 1:
        raise ValueError("quarantine_ratio_threshold must be between 0 and 1")
    if slow_run_seconds <= 0:
        raise ValueError("slow_run_seconds must be positive")

    now = datetime.now(timezone.utc)
    candidates: list[tuple[str, str, Severity, Evidence]] = []

    status = snapshot.status.upper()
    if status in {"FAILED", "FAILURE", "UPSTREAM_FAILED"}:
        evidence = new_evidence(
            "PIPELINE_STATUS",
            f"Pipeline batch finished with status {status}.",
            status=status,
            error_message=snapshot.error_message,
        )
        candidates.append((
            "Pipeline batch failed",
            snapshot.error_message or f"Batch status is {status}.",
            Severity.HIGH,
            evidence,
        ))

    if snapshot.expected_records is not None and snapshot.expected_records > 0:
        if snapshot.records_loaded == 0 and status in {"SUCCESS", "SUCCEEDED"}:
            evidence = new_evidence(
                "ZERO_OUTPUT",
                "The pipeline reported success but loaded zero records.",
                expected_records=snapshot.expected_records,
                records_extracted=snapshot.records_extracted,
                records_loaded=snapshot.records_loaded,
            )
            candidates.append((
                "Successful run produced zero records",
                "A successful batch produced no usable output despite an expected record count.",
                Severity.CRITICAL,
                evidence,
            ))

    if snapshot.records_loaded + snapshot.records_quarantined > 0:
        ratio = snapshot.quarantine_ratio
        if ratio >= quarantine_ratio_threshold and snapshot.records_quarantined > 0:
            severity = Severity.HIGH if ratio >= 0.25 else Severity.MEDIUM
            evidence = new_evidence(
                "QUARANTINE_RATE",
                f"{ratio:.1%} of processed records were quarantined.",
                quarantine_ratio=ratio,
                threshold=quarantine_ratio_threshold,
                records_loaded=snapshot.records_loaded,
                records_quarantined=snapshot.records_quarantined,
            )
            candidates.append((
                "Data quality quarantine threshold exceeded",
                f"Quarantine ratio {ratio:.1%} meets or exceeds threshold {quarantine_ratio_threshold:.1%}.",
                severity,
                evidence,
            ))

    duration = snapshot.duration_seconds
    if duration is not None and duration > slow_run_seconds:
        evidence = new_evidence(
            "RUN_DURATION",
            f"Batch duration {duration:.1f}s exceeded {slow_run_seconds:.1f}s.",
            duration_seconds=duration,
            threshold_seconds=slow_run_seconds,
        )
        candidates.append((
            "Pipeline run exceeded duration threshold",
            "The batch completed more slowly than its configured service threshold.",
            Severity.MEDIUM,
            evidence,
        ))

    incidents: list[Incident] = []
    for title, description, severity, evidence in candidates:
        fingerprint_source = f"{snapshot.pipeline}:{title}"
        fingerprint = hashlib.sha256(fingerprint_source.encode()).hexdigest()[:24]
        incidents.append(Incident(
            incident_id=hashlib.sha256(
                f"{snapshot.batch_id}:{fingerprint}".encode()
            ).hexdigest()[:32],
            fingerprint=fingerprint,
            pipeline=snapshot.pipeline,
            batch_id=snapshot.batch_id,
            title=title,
            description=description,
            severity=severity,
            status=IncidentStatus.OPEN,
            detected_at=now,
            evidence=(evidence,),
        ))
    return incidents
