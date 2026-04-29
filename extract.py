import requests
from datetime import date, timedelta
from config import BOT_BASE_URL, EXCHANGE_PATH, BOT_API_TOKEN

def fetch_exchange_rates(start_date: str, end_date: str) -> dict:
    """Call BOT API for a date range. Returns raw JSON."""
    url = f"{BOT_BASE_URL}{EXCHANGE_PATH}"
    headers = {
        "Authorization": f"Bearer {BOT_API_TOKEN}",
        "Accept": "application/json"
    }
    params = {
        "start_period": start_date,   # format: YYYY-MM-DD
        "end_period":   end_date,
    }
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def parse_response(raw: dict) -> list[dict]:
    """Flatten nested BOT JSON into a list of row dicts."""
    rows = []
    data_list = raw.get("result", {}).get("data", {}).get("data_detail", [])
    for entry in data_list:
        rows.append({
            "period":           entry.get("period"),
            "currency_code":    entry.get("currency_id"),
            "currency_name":    entry.get("currency_name_eng"),
            "buying_sight":     entry.get("buying_sight"),
            "buying_transfer":  entry.get("buying_transfer"),
            "selling":          entry.get("selling"),
            "mid_rate":         entry.get("mid_rate"),
        })
    return rows

def get_last_n_days(n: int = 180) -> list[dict]:
    """Convenience wrapper: fetch + parse the last N calendar days in 90-day chunks."""
    all_rows = []
    end = date.today()
    start = end - timedelta(days=n)
    
    # Fetch in 90-day chunks to respect API limits
    chunk_size = 90
    current_end = end
    
    while current_end > start:
        current_start = max(start, current_end - timedelta(days=chunk_size))
        try:
            raw = fetch_exchange_rates(current_start.isoformat(), current_end.isoformat())
            all_rows.extend(parse_response(raw))
            print(f"  Fetched {current_start.isoformat()} to {current_end.isoformat()}")
        except Exception as e:
            print(f"  Warning: Failed to fetch {current_start.isoformat()} to {current_end.isoformat()}: {e}")
        
        current_end = current_start - timedelta(days=1)
    
    return all_rows