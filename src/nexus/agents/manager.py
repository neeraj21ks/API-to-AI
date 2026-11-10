"""Agent Manager: coordinates bounded agents into one incident report."""
from __future__ import annotations

from datetime import datetime, timezone

from nexus.agents.specialists import (
    investigation_agent, recovery_planner_agent, root_cause_agent,
    triage_agent, verification_agent,
)
from nexus.contracts import BatchSnapshot, Incident, IncidentReport


class AgentManager:
    """Sequential, deterministic orchestration with no autonomous side effects."""

    def investigate(self, incident: Incident, snapshot: BatchSnapshot) -> IncidentReport:
        if incident.batch_id != snapshot.batch_id:
            raise ValueError("Incident and batch snapshot must refer to the same batch")

        triage = triage_agent(incident)
        investigation = investigation_agent(incident, snapshot)
        rca = root_cause_agent(incident, snapshot)
        recovery_plan = recovery_planner_agent(incident, rca)
        checks = verification_agent(snapshot)

        return IncidentReport(
            incident=incident,
            findings=(triage, investigation, rca),
            recovery_plan=recovery_plan,
            verification_checks=checks,
            generated_at=datetime.now(timezone.utc),
        )
