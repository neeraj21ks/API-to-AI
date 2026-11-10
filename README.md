# NEXUS — Autonomous DataOps Platform

NEXUS detects, investigates, explains and safely helps resolve data-pipeline incidents. It combines deterministic observability and data-quality checks with a coordinated set of specialist agents, producing evidence-backed incident reports, root-cause hypotheses, controlled recovery recommendations and independent verification checks.

The existing Binance market-data pipeline is retained as the first real workload and integration target. It exercises batch ingestion, idempotency, data validation, quarantine handling and orchestration failures. **NEXUS is the DataOps product; crypto market data is its initial workload, not its product purpose.**

## Product workflow

1. **Observe:** collect pipeline run metadata, logs, metrics, data-quality results and lineage evidence.
2. **Detect:** apply deterministic rules to identify failures, freshness/volume anomalies, quality regressions and performance degradation.
3. **Coordinate:** the Agent Manager assigns bounded tasks to specialist agents.
4. **Investigate:** triage, investigation and root-cause agents correlate evidence and produce traceable findings.
5. **Plan:** the recovery planner proposes a policy-checked remediation.
6. **Approve:** a human authorizes consequential actions.
7. **Verify:** independent checks confirm recovery and data correctness; all decisions are auditable.

## Current implementation

The first NEXUS foundation lives in `src/nexus/`:

- Typed contracts for batch snapshots, evidence, incidents, findings and recovery plans.
- Deterministic incident rules for failed runs, successful zero-output runs, quarantine spikes and slow runs.
- Specialist agents for triage, investigation, root-cause analysis, recovery planning and verification.
- An Agent Manager that coordinates the workflow and returns one structured report.
- Explicit safety boundary: recommendations are non-executable and require human approval.

The existing Binance pipeline remains intact for now. It has not yet been connected to the NEXUS incident store or agent workflow.

## Run the first NEXUS demo

Python 3.10+:

```powershell
python -m pip install -e ".[dev]"
python -m pytest
nexus-demo
```

If running without installing the package:

```powershell
$env:PYTHONPATH = "src"
python -m nexus.demo
```

## Planned integration sequence

- Pipeline adapters: ingest Airflow run state, batch metadata and structured logs.
- Incident persistence and deduplication: PostgreSQL-backed incidents, evidence and audit history.
- Observability: metrics, traces, freshness/volume checks and lineage context.
- Agentic investigation: LLM-assisted evidence interpretation with strict structured outputs and confidence reporting.
- Recovery governance: policy engine, approval workflow, idempotent action executor and rollback strategy.
- Independent verification: post-action health, data-quality and freshness checks.
- Streaming and scale: event-driven monitoring and Kafka-compatible transport when workload justifies it.
- Product interface: API, operator console, alerting and measurable reliability benchmarks.

NEXUS does not allow an LLM or agent to execute arbitrary SQL, restart infrastructure or mutate production data. Consequential operations must pass deterministic policy checks and explicit approval.
