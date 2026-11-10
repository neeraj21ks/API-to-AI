"""Bounded specialist agents.

These first agents are deterministic and auditable. An LLM can later assist with
hypothesis generation, but it must not replace rule-based detection or policy gates.
"""
from __future__ import annotations

from nexus.contracts import (
    AgentFinding, BatchSnapshot, Incident, RecoveryPlan, Severity,
)


def triage_agent(incident: Incident) -> AgentFinding:
    return AgentFinding(
        agent="triage",
        conclusion=f"{incident.severity.value} severity incident requiring investigation.",
        confidence=1.0,
        evidence_ids=tuple(e.evidence_id for e in incident.evidence),
        details={"severity": incident.severity.value, "pipeline": incident.pipeline},
    )


def investigation_agent(incident: Incident, snapshot: BatchSnapshot) -> AgentFinding:
    evidence_ids = tuple(e.evidence_id for e in incident.evidence)
    details = {
        "batch_status": snapshot.status,
        "records_extracted": snapshot.records_extracted,
        "records_loaded": snapshot.records_loaded,
        "records_quarantined": snapshot.records_quarantined,
        "error_message": snapshot.error_message,
    }
    return AgentFinding(
        agent="investigation",
        conclusion=(
            f"Inspected batch {snapshot.batch_id}: status={snapshot.status}, "
            f"extracted={snapshot.records_extracted}, loaded={snapshot.records_loaded}, "
            f"quarantined={snapshot.records_quarantined}."
        ),
        confidence=1.0,
        evidence_ids=evidence_ids,
        details=details,
    )


def root_cause_agent(incident: Incident, snapshot: BatchSnapshot) -> AgentFinding:
    title = incident.title.lower()
    if "failed" in title:
        category = "EXECUTION_FAILURE"
        hypothesis = snapshot.error_message or "The pipeline reported a failed state; inspect task-level logs."
        confidence = 0.85 if snapshot.error_message else 0.55
    elif "zero records" in title:
        category = "EMPTY_OUTPUT"
        hypothesis = "The extraction, filtering, or upstream source may have returned no usable records."
        confidence = 0.65
    elif "quarantine" in title:
        category = "DATA_QUALITY"
        hypothesis = "Incoming records violate one or more validation rules; inspect quarantined samples."
        confidence = 0.75
    else:
        category = "PERFORMANCE"
        hypothesis = "The batch exceeded its duration threshold; inspect task timings and source latency."
        confidence = 0.6
    return AgentFinding(
        agent="root_cause_analysis",
        conclusion=hypothesis,
        confidence=confidence,
        evidence_ids=tuple(e.evidence_id for e in incident.evidence),
        details={"category": category, "hypothesis": hypothesis, "confirmed": False},
    )


def recovery_planner_agent(incident: Incident, rca: AgentFinding) -> RecoveryPlan:
    """Produce recommendations only; no infrastructure or data mutation occurs."""
    category = rca.details.get("category")
    actions_by_category = {
        "EXECUTION_FAILURE": (
            "Inspect the failed Airflow task and its structured logs.",
            "Validate source/API availability and database connectivity.",
            "Retry only after confirming the failure is transient and the batch is idempotent.",
        ),
        "EMPTY_OUTPUT": (
            "Check source response size and extraction time window.",
            "Compare extracted, transformed, and loaded record counts.",
            "Verify filters and watermark boundaries before replaying the batch.",
        ),
        "DATA_QUALITY": (
            "Sample quarantined rows and group them by validation reason.",
            "Check schema drift and upstream field/type changes.",
            "Replay only after validation rules or source data are corrected.",
        ),
        "PERFORMANCE": (
            "Compare task-level durations with recent successful runs.",
            "Inspect source latency, database wait time, and resource saturation.",
            "Tune concurrency or batch sizing only after identifying the bottleneck.",
        ),
    }
    actions = actions_by_category.get(category, ("Collect additional logs and metrics before recovery.",))
    return RecoveryPlan(
        summary=f"Controlled recovery recommendations for {incident.title}.",
        actions=actions,
        requires_human_approval=True,
        executable=False,
    )


def verification_agent(snapshot: BatchSnapshot) -> tuple[str, ...]:
    return (
        "Confirm the rerun reaches a terminal successful state.",
        "Confirm loaded record count meets the expected-volume contract.",
        "Confirm duplicate/idempotency checks pass.",
        "Confirm quarantine ratio is below the configured threshold.",
        "Confirm downstream dbt tests and freshness checks pass.",
        "Retain incident, approval, action and verification evidence in the audit trail.",
    )
