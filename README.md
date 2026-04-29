# BOT Exchange Rate Pipeline

## Description
A data engineering project that extracts daily FX rates from the Bank of Thailand(BOT) API, 
loads them into BigQuery, transforms with dbt, and visualizes in Looker Studio.

---

## Architecture
![Alt text](bot_pipeline_architecture.svg)

---

## Tech Stack
| Layer | Tool |
|---|---|
| Extraction | Python · `requests` · `pandas` |
| Storage | Google BigQuery |
| Transformation | dbt (`dbt-bigquery`) |
| Visualisation | Looker Studio |
| Credentials | `.env` · `python-dotenv` · GCP service account |

---

## How to run
1. Clone the repo
2. Create `.env` with your BOT API token and GCP credentials
3. Run `pip install -r requirements.txt` to install libraries
4. Run `python pipeline.py` to load data
5. Run `dbt run && dbt test` in the `bot_exchange/` folder

---

## Dashboard
[Looker Studio dashboard](https://datastudio.google.com/reporting/6c29fd37-0710-4948-bc6d-6dbb2f767979)

---

## Challenges & Solutions

### 1. BOT API endpoint changed — old URL returns 404
The API base URL (`https://apigw1.bot.or.th/bot/public`) and header (`{"X-IBM-Client-Id": bot_token, "Accept": "application/json"}`)  documented in older tutorials returned 404.

Register on the new portal, subscribe to the Exchange Rates plan, and update `config.py` with the correct base URL and path:
```python
BOT_BASE_URL  = "https://gateway.api.bot.or.th"
EXCHANGE_PATH = "/Stat-ExchangeRate/v2/DAILY_AVG_EXG_RATE/"
```
and correct header
```python
headers = {
    "Authorization": f"Bearer {BOT_API_TOKEN}",
    "Accept": "application/json"
}
```

### 2. Python / dbt-bigquery version incompatibility
After `pip install dbt-bigquery`, running `dbt run` immediately threw the error.

Pin to a version that supports your Python:
| Python | min dbt-bigquery |
|---|---|
| 3.13 | `>=1.9.x` |

### 3. Transformation timeout — processing all rows at once
Running `extract.py` on the full date range caused the process to hang and eventually crash with a memory error on larger pulls.
Rewrote `extract.py` to process data in chunks using a date-range loop 90-day chunks to respect API limits:

---
 
## License
 
MIT