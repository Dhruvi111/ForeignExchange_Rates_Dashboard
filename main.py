from datetime import date, timedelta
from components.data_import import fetch_exchange_rates
from components.data_cleaning import clean_fx_data
from components.data_load import load_to_bigquery
from components.logger import get_logger

logger = get_logger(__name__)

def run_pipeline():
    # Always fetch yesterday's data (most recent complete day)
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    logger.info(f"Running pipeline for {yesterday}")
    
    data     = fetch_exchange_rates(start_date=yesterday, end_date=yesterday)
    pkl_path = clean_fx_data(data)
    load_to_bigquery(pkl_path)
    
    logger.info("Pipeline complete.")

if __name__ == "__main__":
    run_pipeline()