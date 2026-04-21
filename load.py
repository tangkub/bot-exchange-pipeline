from google.cloud import bigquery
from config import GCP_PROJECT_ID, BQ_DATASET, BQ_TABLE
import pandas as pd

def create_dataset_if_not_exists(client: bigquery.Client):
    dataset_ref = f"{GCP_PROJECT_ID}.{BQ_DATASET}"
    try:
        client.get_dataset(dataset_ref)
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "asia-southeast1"
        client.create_dataset(dataset)
        print(f"Created dataset {dataset_ref}")

def load_to_bigquery(df: pd.DataFrame):
    client = bigquery.Client(project=GCP_PROJECT_ID)
    create_dataset_if_not_exists(client)

    table_ref = f"{GCP_PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",   # Change to WRITE_APPEND for adding new rows to the existing table
        autodetect=True,                    # Infer schema from DataFrame
    )

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()   # Block until done

    table = client.get_table(table_ref)
    print(f"Loaded {len(df)} rows → {table_ref} (total {table.num_rows} rows)")