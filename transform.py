import pandas as pd

NUMERIC_COLS = ["buying_sight", "buying_transfer", "selling", "mid_rate"]

def clean_data(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    df["period"] = pd.to_datetime(df["period"])

    # Coerce rate columns to float (BOT sometimes returns "-" for illiquid rates)
    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Derived column: bid-ask spread as % of mid
    df["spread_pct"] = (
        (df["selling"] - df["buying_transfer"]) / df["mid_rate"] * 100
    ).round(4)

    # Drop full duplicates (same date + currency) keeping first occurrence
    df = df.drop_duplicates(subset=["period", "currency_code"])

    return df.reset_index(drop=True)

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    # Must have rows
    if df.empty:
        raise ValueError("DataFrame is empty after cleaning.")

    # period and currency_code must be present
    nulls = df[["period", "currency_code"]].isnull().sum()
    if nulls.any():
        raise ValueError(f"Null values in key columns:\n{nulls[nulls > 0]}")

    # Rates must be positive when present
    for col in NUMERIC_COLS:
        bad = df[col].dropna()
        if (bad <= 0).any():
            raise ValueError(f"Non-positive values found in {col}")

    print(f"Validation passed — {len(df)} rows, {df['currency_code'].nunique()} currencies.")
    return df