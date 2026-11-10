"""Run a local, dependency-free NEXUS incident investigation demo."""
from datetime import datetime, timedelta, timezone
import json

from nexus.agents.manager import AgentManager
from nexus.contracts import BatchSnapshot
from nexus.detection.rules import detect_incidents


def main() -> None:
    now = datetime.now(timezone.utc)
    snapshot = BatchSnapshot(
        pipeline="crypto_market_data_pipeline",
        batch_id="demo-batch-001",
        status="FAILED",
        started_at=now - timedelta(minutes=3),
        completed_at=now,
        records_extracted=30,
        records_loaded=24,
        records_quarantined=6,
        expected_records=30,
        error_message="Simulated upstream timeout after partial ingestion",
        source="binance",
    )
    incidents = detect_incidents(snapshot)
    manager = AgentManager()
    reports = [manager.investigate(incident, snapshot) for incident in incidents]
    print(json.dumps([report.to_dict() for report in reports], indent=2))


if __name__ == "__main__":
    main()
