---
name: setup-pipeline-etl
description: >
  Generates ETL pipeline scaffolding with source extraction, transformation logic, load targets,
  error handling, and logging for data engineering workflows. Use this skill whenever the user wants
  to build an ETL pipeline, design a data ingestion workflow, implement data transformation logic,
  set up data loading to a warehouse, or asks to "build an ETL pipeline", "set up data ingestion",
  "implement an extract-transform-load process", "create a data pipeline", "build a pipeline to
  move data from X to Y", "set up Airflow DAG for ETL", "write a PySpark transformation", or
  "create a data processing pipeline". Also trigger for "ELT pipeline", "data ingestion", "batch
  processing pipeline", "streaming ETL", "Airflow DAG", "Prefect flow", and "Luigi pipeline".
  Distinct from model-dbt (which handles SQL transformations in dbt) and setup-rag (which builds
  retrieval pipelines for AI).
---

# setup-pipeline-etl

Generate an **ETL pipeline** with extraction, transformation, loading, error handling, and observability.

## Pipeline architecture selection

Detect the appropriate approach from context:

| Approach | Best for | Tools |
|----------|----------|-------|
| **Airflow** | Complex DAGs, scheduling, team collaboration | Apache Airflow |
| **Prefect** | Modern Python, simpler setup than Airflow | Prefect 2.x |
| **Python scripts** | Simple one-off or scheduled pipelines | Python + cron |
| **Spark** | Large-scale distributed processing | PySpark |
| **dbt** | SQL-only transformations in existing DWH | dbt (use model-dbt skill) |

Default to **Python + Prefect** for new pipelines (simpler than Airflow, production-ready).

## Information gathering

From context, identify:
- **Source**: Database, REST API, files (CSV/JSON/Parquet), message queue, SaaS tool?
- **Target**: Data warehouse (Snowflake, BigQuery, Redshift), database, S3, another system?
- **Transformation**: What business logic, cleaning, enrichment?
- **Schedule**: One-time, hourly, daily, event-triggered?
- **Volume**: Rows/day, data size? (affects batch vs streaming choice)
- **Orchestrator preference**: Airflow, Prefect, cron, none?

## Pipeline template (Prefect)

```python
# etl/pipeline.py

import logging
from datetime import datetime, timedelta
from typing import Iterator
import pandas as pd
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash

# ─── Configuration ────────────────────────────────────────────────────────

SOURCE_DB_URL = "postgresql://user:pass@host:5432/source_db"
TARGET_DB_URL = "postgresql://user:pass@host:5432/warehouse"
BATCH_SIZE = 10_000

# ─── Extraction ───────────────────────────────────────────────────────────

@task(
    name="extract-from-source",
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=1),
    retries=3,
    retry_delay_seconds=60,
)
def extract(last_run_at: datetime) -> pd.DataFrame:
    """Extract records from source DB modified since last run."""
    logger = get_run_logger()
    
    query = """
        SELECT id, customer_id, amount, status, created_at, updated_at
        FROM orders
        WHERE updated_at > %(last_run_at)s
        ORDER BY updated_at ASC
        LIMIT %(batch_size)s
    """
    
    df = pd.read_sql(
        query,
        SOURCE_DB_URL,
        params={"last_run_at": last_run_at, "batch_size": BATCH_SIZE}
    )
    
    logger.info(f"Extracted {len(df)} records from source")
    return df

# ─── Transformation ───────────────────────────────────────────────────────

@task(name="transform-orders")
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Apply business logic transformations."""
    logger = get_run_logger()
    
    if df.empty:
        logger.info("No records to transform")
        return df
    
    # Data quality checks
    null_counts = df.isnull().sum()
    if null_counts["customer_id"] > 0:
        logger.warning(f"Found {null_counts['customer_id']} records with null customer_id")
    
    # Transformations
    df = df.copy()
    
    # Normalize: strip whitespace from string columns
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())
    
    # Derive: map status to numeric
    STATUS_MAP = {"pending": 0, "confirmed": 1, "shipped": 2, "delivered": 3, "cancelled": -1}
    df["status_code"] = df["status"].map(STATUS_MAP).fillna(-99)
    
    # Derive: revenue in USD (assuming cents input)
    df["amount_usd"] = (df["amount"] / 100).round(2)
    
    # Derive: fiscal quarter
    df["fiscal_quarter"] = pd.PeriodIndex(df["created_at"], freq="Q").strftime("Q%q %Y")
    
    # Drop originals where derived replaces them
    df = df.drop(columns=["amount"])
    
    # Validate output schema
    required_cols = {"id", "customer_id", "amount_usd", "status", "status_code", "created_at"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Transformation produced incomplete schema: missing {missing}")
    
    logger.info(f"Transformed {len(df)} records")
    return df

# ─── Loading ──────────────────────────────────────────────────────────────

@task(name="load-to-warehouse", retries=2)
def load(df: pd.DataFrame, table_name: str = "fact_orders") -> int:
    """Load transformed data to target warehouse (upsert)."""
    from sqlalchemy import create_engine, text
    
    logger = get_run_logger()
    
    if df.empty:
        logger.info("Nothing to load")
        return 0
    
    engine = create_engine(TARGET_DB_URL)
    
    # Write to staging table first
    staging_table = f"{table_name}_staging"
    df.to_sql(staging_table, engine, if_exists="replace", index=False, method="multi", chunksize=1000)
    
    # Upsert from staging to target
    with engine.begin() as conn:
        conn.execute(text(f"""
            INSERT INTO {table_name} ({", ".join(df.columns)})
            SELECT {", ".join(df.columns)} FROM {staging_table}
            ON CONFLICT (id) DO UPDATE SET
                {", ".join(f"{col} = EXCLUDED.{col}" for col in df.columns if col != "id")}
        """))
        conn.execute(text(f"DROP TABLE IF EXISTS {staging_table}"))
    
    logger.info(f"Loaded {len(df)} records to {table_name}")
    return len(df)

# ─── State management ─────────────────────────────────────────────────────

def get_last_run_time() -> datetime:
    """Get the timestamp of the last successful run from state store."""
    # In production: read from a pipeline state table or file
    # Fallback to 24 hours ago
    try:
        with open(".pipeline_state") as f:
            return datetime.fromisoformat(f.read().strip())
    except FileNotFoundError:
        return datetime.utcnow() - timedelta(days=1)

def save_last_run_time(dt: datetime):
    with open(".pipeline_state", "w") as f:
        f.write(dt.isoformat())

# ─── Main flow ────────────────────────────────────────────────────────────

@flow(
    name="orders-etl",
    description="Extract orders from source DB, transform, and load to warehouse",
    on_failure=[notify_on_failure],     # Optional: add alerting
)
def orders_etl_flow():
    logger = get_run_logger()
    
    run_start = datetime.utcnow()
    last_run = get_last_run_time()
    
    logger.info(f"Starting ETL run. Last run: {last_run}")
    
    # Run ETL
    raw = extract(last_run_at=last_run)
    transformed = transform(raw)
    records_loaded = load(transformed)
    
    # Save state only on success
    save_last_run_time(run_start)
    
    logger.info(f"ETL complete. Loaded {records_loaded} records.")
    return records_loaded


if __name__ == "__main__":
    orders_etl_flow()
```

## Deployment

```python
# deploy.py — schedule the flow
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from pipeline import orders_etl_flow

Deployment.build_from_flow(
    flow=orders_etl_flow,
    name="orders-etl-daily",
    schedule=CronSchedule(cron="0 3 * * *", timezone="UTC"),  # 3 AM UTC daily
    tags=["etl", "orders"],
).apply()
```

## Error handling patterns

```python
# Notification on failure
from prefect import flow
from prefect.blocks.notifications import SlackWebhook

async def notify_on_failure(flow, flow_run, state):
    slack = await SlackWebhook.load("etl-alerts")
    await slack.notify(
        body=f"❌ ETL flow '{flow.name}' failed: {state.message}",
    )

# Dead letter queue for failed records
def load_with_dlq(df: pd.DataFrame, table_name: str):
    failed = []
    for batch in chunk(df, 1000):
        try:
            batch.to_sql(table_name, engine, if_exists="append")
        except Exception as e:
            logger.error(f"Batch failed: {e}")
            failed.extend(batch.to_dict("records"))
    
    if failed:
        pd.DataFrame(failed).to_sql(f"{table_name}_dlq", engine, if_exists="append")
        logger.warning(f"{len(failed)} records sent to DLQ")
```

## Observability

```python
# Add metrics to each task
from prometheus_client import Counter, Histogram, start_http_server

RECORDS_EXTRACTED = Counter("etl_records_extracted_total", "Total records extracted", ["pipeline"])
RECORDS_LOADED = Counter("etl_records_loaded_total", "Total records loaded", ["pipeline", "table"])
PIPELINE_DURATION = Histogram("etl_pipeline_duration_seconds", "Pipeline run duration", ["pipeline"])
```

## Calibration

- **API source**: Show pagination logic, rate limiting, auth headers
- **File source (S3/GCS)**: Show file listing, incremental processing by modification date
- **Streaming (Kafka)**: Show consumer group, offset management, micro-batching
- **Airflow**: Show DAG definition with operators instead of Prefect flow/task
- **Large volume**: Show chunked processing, parallel workers, memory management
