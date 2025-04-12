# src/data_ingestion.py
import os
import pandas as pd
import requests
import time

TICKERS = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
API_KEY = "demo"  # Replace with your actual FMP API Key
OUTPUT_DIR = "../data"
BASE_URL = "https://financialmodelingprep.com/api/v3"


def fetch_stock(symbol):
    url = f"{BASE_URL}/historical-price-full/{symbol}?apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data['historical'])
    df['ticker'] = symbol
    return df


def fetch_and_save_data():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for ticker in TICKERS:
        try:
            df = fetch_stock(ticker)
            df.to_csv(f"{OUTPUT_DIR}/{ticker}.csv", index=False)
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
