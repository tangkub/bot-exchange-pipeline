import os
from dotenv import load_dotenv

load_dotenv()

BOT_BASE_URL = "https://gateway.api.bot.or.th"
EXCHANGE_PATH = "/Stat-ExchangeRate/v2/DAILY_AVG_EXG_RATE/"

BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BQ_DATASET = os.getenv("BQ_DATASET", "bot_exchange")
BQ_TABLE = os.getenv("BQ_TABLE", "daily_rates")