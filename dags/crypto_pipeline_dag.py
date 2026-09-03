from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.pipeline import run_pipeline


def execute_crypto_pipeline():
    batch_id = run_pipeline()
    print(f"Pipeline completed successfully. Batch ID: {batch_id}")


with DAG(
    dag_id="crypto_market_data_pipeline",
    start_date=datetime(2026, 9, 1),
    schedule="*/5 * * * *",
    catchup=False,
    tags=["crypto", "binance", "data-engineering"],
) as dag:

    run_crypto_pipeline = PythonOperator(
        task_id="run_crypto_pipeline",
        python_callable=execute_crypto_pipeline,
    )