import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import time

def read_tickers_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        tickers = df['Ticker'].dropna().unique().tolist()
        return tickers
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

def download_and_save(ticker, start, end):
    print(f"Downloading {ticker} from {start} to {end}...")
    data = yf.download(ticker, start=start, end=end + timedelta(days=1), threads=False)
    if data.empty:
        print(f"No data for {ticker}")
        return

    df = data[['Close']].copy()
    df.reset_index(inplace=True)
    filename = f"{ticker}.csv"

    if os.path.exists(filename):
        existing = pd.read_csv(filename, parse_dates=['Date'])
        last_date = existing['Date'].max().date()
        df = df[df['Date'] > pd.to_datetime(last_date)]
        combined = pd.concat([existing, df]).drop_duplicates(subset='Date').sort_values('Date')
    else:
        combined = df

    combined.to_csv(filename, index=False)
    print(f"Saved {ticker} to {filename}")

def main():
    file_path = input("Enter path to CSV with tickers: ___ (default: 'Ticker.csv'): ") or "Ticker.csv"
    tickers = read_tickers_from_csv(file_path="Ticker.csv")
    if not tickers:
        return

    end = datetime.today().date()
    start = end - timedelta(days=30)

    for ticker in tickers:
        download_and_save(ticker, start, end)
        time.sleep(10)  # ⏱️ 2-second delay between requests

if __name__ == "__main__":
    main()
