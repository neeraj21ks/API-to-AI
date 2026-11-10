# NEXUS — Autonomous DataOps Platform

NEXUS is evolving from the existing API-to-AI market-data pipeline into an autonomous DataOps platform. Its product promise is to **detect, investigate, explain, and safely resolve data-pipeline incidents**. The current Binance ingestion workload is retained as the first workload used to build and validate the platform.

## Current engineering baseline

- Python ingestion and validation
- Binance public REST API as the initial data source
- PostgreSQL 16 for local development and durable pipeline state
- Docker Compose for reproducible local infrastructure
- Apache Airflow for orchestration (existing DAG retained)
- dbt, streaming, observability, and agentic incident workflows are subsequent milestones

## Local development setup

### Prerequisites

- Docker Desktop with the Docker Compose plugin
- Python 3.11+
- Git

### 1. Configure environment

PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set a strong local `POSTGRES_PASSWORD`. Set `DATABASE_URL` to use the same password:

```text
DATABASE_URL=postgresql://nexus:YOUR_PASSWORD@localhost:5432/nexus
```

Do not commit `.env` or put real credentials in source code. `.env.example` contains placeholders only.

### 2. Start PostgreSQL

```powershell
docker compose up -d postgres
docker compose ps
docker compose logs -f postgres
```

PostgreSQL listens on `localhost:5432` by default. The named Docker volume `nexus_postgres_data` persists data across container restarts.

The schema in `sql/schema.sql` is mounted into the container's initialization directory. PostgreSQL applies it only when the data directory is first initialized. If you change the bootstrap schema and intentionally want a fresh local database, run:

```powershell
docker compose down -v
docker compose up -d postgres
```

**Warning:** `docker compose down -v` deletes the local PostgreSQL volume and all data stored in it.

### 3. Install the Python project

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

If the Python launcher is unavailable, create the virtual environment with your installed Python 3.11+ executable.

### 4. Verify the database

```powershell
docker compose exec postgres pg_isready -U nexus -d nexus
```

The initial schema creates `pipeline_batches`, `raw_events`, and `clean_events`.

## Repository layout

```text
.
├── dags/                 # Airflow DAG definitions
├── dbt/                  # dbt project
├── sql/schema.sql        # PostgreSQL bootstrap schema
├── src/
│   ├── db.py             # Shared PostgreSQL connection factory
│   ├── extract.py        # Side-effect-free Binance extraction client
│   ├── kline_process.py  # Record transformation and validation flow
│   ├── load.py           # Raw and clean PostgreSQL persistence
│   └── pipeline.py       # Batch orchestration
├── docker-compose.yml    # Local PostgreSQL service
├── .env.example          # Safe environment template
└── pyproject.toml        # Runtime and development dependencies
```

## Reliability principles being established

- Importing a Python module must not start network requests or mutate the database.
- One PostgreSQL driver (Psycopg 3) is used consistently.
- Clean-event writes participate in an explicit transaction.
- Database write failures propagate to the orchestrator; they must not be logged and silently treated as success.
- Pipeline batch status and record counts are persisted for later observability.
- Credentials remain outside source control.

## Product roadmap

1. **Phase 0 — Repository and local infrastructure foundation:** configuration hygiene, Dockerized PostgreSQL, schema consistency, deterministic imports, and reliable database writes.
2. **Phase 1 — Pipeline reliability:** automated tests, data-quality contracts, retry/backoff policy, idempotency, quarantine persistence, and failure-injection scenarios.
3. **Phase 2 — Data observability:** freshness, volume, schema, and distribution monitoring; incident events; lineage and run history.
4. **Phase 3 — Agentic investigation:** an agent manager coordinating specialized triage, investigation, root-cause, and recovery-planning agents. Tools are constrained, actions audited, and risky recovery requires human approval.
5. **Phase 4 — Safe remediation and verification:** policy-gated runbooks, approval workflows, post-action verification, rollback paths, and measurable recovery benchmarks.
6. **Phase 5 — Scale-out:** Kafka/PySpark streaming, dbt integration, service APIs, dashboards, and deployment hardening.

NEXUS is a DataOps engineering product, not an autonomous trading or investment recommendation system.
