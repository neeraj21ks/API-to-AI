"""Typed contracts shared by NEXUS detection and agent workflows."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


@dataclass(frozen=True)
class BatchSnapshot:
    """Normalized observation of one pipeline run; adapters populate this later."""

    pipeline: str
    batch_id: str
    status: str
    started_at: datetime
    completed_at: datetime | None = None
    records_extracted: int = 0
    records_loaded: int = 0
    records_quarantined: int = 0
    expected_records: int | None = None
    error_message: str | None = None
    source: str = "unknown"

    @property
    def duration_seconds(self) -> float | None:
        if self.completed_at is None:
            return None
        return max(0.0, (self.completed_at - self.started_at).total_seconds())

    @property
    def quarantine_ratio(self) -> float:
        total = self.records_loaded + self.records_quarantined
        return self.records_quarantined / total if total else 0.0


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    kind: str
    summary: str
    observed_at: datetime
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Incident:
    incident_id: str
    fingerprint: str
    pipeline: str
    batch_id: str
    title: str
    description: str
    severity: Severity
    status: IncidentStatus
    detected_at: datetime
    evidence: tuple[Evidence, ...] = ()


@dataclass(frozen=True)
class AgentFinding:
    agent: str
    conclusion: str
    confidence: float
    evidence_ids: tuple[str, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RecoveryPlan:
    summary: str
    actions: tuple[str, ...]
    requires_human_approval: bool = True
    executable: bool = False


@dataclass(frozen=True)
class IncidentReport:
    incident: Incident
    findings: tuple[AgentFinding, ...]
    recovery_plan: RecoveryPlan
    verification_checks: tuple[str, ...]
    generated_at: datetime

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly representation for APIs, logs and persistence."""
        data = asdict(self)
        data["incident"]["severity"] = self.incident.severity.value
        data["incident"]["status"] = self.incident.status.value
        data["generated_at"] = self.generated_at.isoformat()
        data["incident"]["detected_at"] = self.incident.detected_at.isoformat()
        for evidence in data["incident"]["evidence"]:
            evidence["observed_at"] = evidence["observed_at"].isoformat()
        return data


def new_evidence(kind: str, summary: str, **details: Any) -> Evidence:
    return Evidence(
        evidence_id=str(uuid4()),
        kind=kind,
        summary=summary,
        observed_at=datetime.now(timezone.utc),
        details=details,
    )
