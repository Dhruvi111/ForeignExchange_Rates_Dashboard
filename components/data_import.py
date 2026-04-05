import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# called at module level so the .env is loaded as soon as the file is imported 
load_dotenv()    



# API only returns 1000 rows per call. Therefore pulling the data in small batches. Logic:-
# Starts with a max batch size (default 7 days).
# Calls API for current batch.
# If len(data) >= 1000 → API limit hit → reduce batch size by half and retry.
# If batch succeeds → append data and move to next batch.
# Continues until current_start > end.
# Dynamically adjusts batch size based on actual data returned.
# Returns a complete DataFrame with all historical data.


import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_exchange_rates(start_date: str, end_date: str, max_batch_days: int = 7) -> pd.DataFrame:
    """
    Fetch exchange rate data from API safely, adjusting batch size if API row limit (1000) is hit.

    Parameters:
        start_date (str): 'YYYY-MM-DD' start date
        end_date (str): 'YYYY-MM-DD' end date
        max_batch_days (int): initial maximum number of days to fetch per batch

    Returns:
        pd.DataFrame: Combined historical data
    """

    base_url = os.getenv("API_BASE_URL")
    if not base_url:
        raise ValueError("API_BASE_URL is not set. Please add it to your .env file.")
    
    all_data = []

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    current_start = start
    batch_days = max_batch_days

    while current_start <= end:
        current_end = current_start + timedelta(days=batch_days - 1)
        if current_end > end:
            current_end = end

        params = {
            "startDate": current_start.strftime("%Y-%m-%d"),
            "endDate": current_end.strftime("%Y-%m-%d")
        }

        try:
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            # The data returned is a dictionary with a key "ForeignExchangeRates"
            # The value of that key is a list of dictionaries. Dictionaries has the fx data

            # Extract the list under 'ForeignExchangeRates'
            rates_list = data.get("ForeignExchangeRates", [])
            row_count = len(rates_list)
            print(f"Fetched {row_count} rows: {params['startDate']} → {params['endDate']}")

            if row_count >= 1000:
                # API limit hit → shrink batch and retry
                if batch_days == 1:
                    # cannot shrink further, accept possible truncation
                    all_data.extend(rates_list)
                    current_start += timedelta(days=1)
                else:
                    batch_days = max(1, batch_days // 2)
                    print(f"API limit hit. Reducing batch size to {batch_days} day(s) and retrying...")
                    continue  # retry smaller batch
            else:
                # safe, append data and move to next batch
                all_data.extend(rates_list)
                current_start = current_end + timedelta(days=1)
                batch_days = max_batch_days  # reset batch size

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {params}: {e}")
            # Move one day ahead to avoid infinite loop
            current_start += timedelta(days=1)

    # Convert flat list of dicts into DataFrame
    df = pd.json_normalize(all_data)            # json.normalize expects a flat list of dicts as input
    print(f"Total rows fetched: {len(df)}")
    return df

print("Test. It runs")
# data=fetch_exchange_rates(start_date="2026-02-15",end_date="2026-02-28")
# print(data.head())