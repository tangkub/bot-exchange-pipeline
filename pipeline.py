from extract import get_last_n_days
from transform import clean_data, validate_data
from load import load_to_bigquery

def run_pipeline(days: int = 30):
    print(f"--- Extracting last {days} days ---")
    raw_rows = get_last_n_days(days)
    print(f"Fetched {len(raw_rows)} raw records")

    print("--- Transforming ---")
    df = clean_data(raw_rows)

    print("--- Validating ---")
    df = validate_data(df)

    print("--- Loading to BigQuery ---")
    load_to_bigquery(df)

    print("Pipeline complete.")

if __name__ == "__main__":
    run_pipeline()