API-to-AI

A production-grade data engineering pipeline built on live Binance market data — batch and streaming, from a single REST call to a cloud-scale warehouse.

API-to-AI ingests cryptocurrency market data directly from the Binance public API — historical OHLCV kline data via REST, and genuine high-frequency trade events via the WebSocket stream — and pushes it through a progressively more sophisticated pipeline: from a simple batch load into Postgres, through orchestrated dimensional modeling, real-time streaming with Kafka and PySpark, and finally a cloud-native data warehouse on AWS.

Binance was chosen deliberately over synthetic or bulk-download data sources: its WebSocket feed delivers real high-frequency trade events with no API key required, closing the "simulated volume" gap common in portfolio projects and giving every downstream milestone genuine production-like data to work with.

Stack: Python · pandas · psycopg2 · PostgreSQL · Apache Airflow (Docker Compose) · dbt-core · Apache Kafka · PySpark · Redis · AWS S3 · Redshift · Streamlit

Architecture

The project is built in five milestones, each layering new infrastructure on top of the last:

#	Milestone	What it adds
1	Batch pipeline	REST API → pandas → PostgreSQL
2	Orchestration	Airflow + dbt, dimensional modeling with an SCD Type 2 star schema
3	Streaming	Kafka producer from the WebSocket feed + PySpark Structured Streaming with watermarking
4	Cloud migration	S3 data lake + Redshift, with distribution and sort keys tuned for query patterns
5	Observability	Streamlit dashboard with monitoring, alerting, and failure injection for behavioral interview stories
Roadmap


 Milestone 1 — Batch pipeline: REST → pandas → Postgres
 Milestone 2 — Airflow + dbt orchestration, SCD Type 2 star schema (in progress)
 Milestone 3 — Kafka + PySpark Structured Streaming
 Milestone 4 — S3 data lake + Redshift migration
 Milestone 5 — Streamlit monitoring dashboard
