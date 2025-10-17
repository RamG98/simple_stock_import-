import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

def get_user_input():
    default_ticker = 'AAPL'
    default_end = datetime.today().date()
    default_start = default_end - timedelta(days=90)

    ticker = input(f"Enter ticker (default: {default_ticker}): ") or default_ticker
    end_str = input(f"Enter end date YYYY-MM-DD (default: {default_end}): ") or str(default_end)

    try:
        end = pd.to_datetime(end_str).date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return None, None, None

    return ticker.upper(), end

def get_existing_data(ticker):
    filename = f"{ticker}.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename, parse_dates=['Date'])
        return df
    return None

def download_data(ticker, start, end):
    print(f"Downloading {ticker} data from {start} to {end}...")
    data = yf.download(ticker, start=start, end=end + timedelta(days=1), threads=False)
    if data.empty:
        print("No data found.")
        return None
    data = data[['Close']].copy()
    data.reset_index(inplace=True)
    return data

def save_data(ticker, new_data, existing_data=None):
    filename = f"{ticker}.csv"
    if existing_data is not None:
        combined = pd.concat([existing_data, new_data]).drop_duplicates(subset='Date').sort_values('Date')
    else:
        combined = new_data
    combined.to_csv(filename, index=False)
    print(f"Saved to {filename}")

def main():
    ticker, end = get_user_input()
    if not ticker:
        return

    existing_data = get_existing_data(ticker)
    if existing_data is not None:
        last_date = existing_data['Date'].max().date()
        start = last_date + timedelta(days=1)
        if start > end:
            print("Data is already up to date.")
            return
    else:
        start = end - timedelta(days=90)

    new_data = download_data(ticker, start, end)
    if new_data is not None and not new_data.empty:
        save_data(ticker, new_data, existing_data)

if __name__ == "__main__":
    main()

