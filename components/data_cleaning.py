"""
Typical pipeline:
    data     = fetch_exchange_rates(start_date="2025-01-01", end_date="2026-04-04")
    pkl_path = clean_fx_data(data, output_path="fx_cleaned_data.pkl")
    load_to_bigquery(pkl_path)
"""

import pandas as pd
from logger import get_logger

logger = get_logger(__name__)


def clean_fx_data(
    data: pd.DataFrame,
    output_path: str = "fx_cleaned_data.pkl",
) -> str:
    """
    Clean and transform a raw FX exchange rate DataFrame, then save as a pickle file ready for BigQuery ingestion.

    Parameters
    ----------
    data : pd.DataFrame
        Raw DataFrame returned by fetch_exchange_rates().
    output_path : str, optional
        File path for the output pickle file. Defaults to "fx_cleaned_data.pkl".

    Returns
    -------
    str
        The path to the saved pickle file.
    """

    logger.info(f"Starting data cleaning — initial shape: {data.shape}")

    # ------------------------------------------------------------------
    # 1. Check and handle missing / null values
    # ------------------------------------------------------------------
    missing_counts = data.isnull().sum()
    total_missing = missing_counts.sum()

    if total_missing > 0:
        logger.warning(f"Found {total_missing} missing values across columns:")
        for col, count in missing_counts[missing_counts > 0].items():
            logger.warning(f"  {col}: {count} missing")
        data = data.dropna()
        logger.info(f"Dropped rows with missing values — shape after drop: {data.shape}")
    else:
        logger.info("No missing values found.")

    # ------------------------------------------------------------------
    # 2. Rename specific columns with verbose original names
    # ------------------------------------------------------------------
    data = data.rename(columns={
        "ExchangeRateEffectiveTimestamp": "effective_timestamp",
        "ExchangeRateExpiryTimestamp":    "expiry_timestamp",
        "ExchangeRateSource":             "source",
        "FromCurrency.Value":             "from_currency",
        "ToCurrency.Value":               "to_currency",
    })

    # ------------------------------------------------------------------
    # 3. Normalise ALL column names to lowercase snake_case
    # ------------------------------------------------------------------
    data.columns = (
        data.columns
        .str.strip()
        .str.replace(".", "_", regex=False)
        .str.replace(" ", "_", regex=False)
        .str.lower()
    )

    # ------------------------------------------------------------------
    # 4. Cast data types
    # ------------------------------------------------------------------
    data["rate"] = pd.to_numeric(data["rate"], errors="coerce")

    data["effective_timestamp"] = pd.to_datetime(
        data["effective_timestamp"], errors="coerce"
    )
    data["expiry_timestamp"] = pd.to_datetime(
        data["expiry_timestamp"], errors="coerce"
    )

    # ------------------------------------------------------------------
    # 5. Extract plain date column from effective_timestamp
    # ------------------------------------------------------------------
    data["date"] = pd.to_datetime(data["effective_timestamp"].dt.date)

    # ------------------------------------------------------------------
    # 6. Drop unused columns
    # ------------------------------------------------------------------
    cols_to_drop = [
        col for col in ["fromcurrencycsn", "tocurrencycsn", "expiry_timestamp"]
        if col in data.columns
    ]
    data = data.drop(columns=cols_to_drop)

    # ------------------------------------------------------------------
    # 7. Add currency_pair column
    # ------------------------------------------------------------------
    data["currency_pair"] = data["from_currency"] + "/" + data["to_currency"]

    # ------------------------------------------------------------------
    # 8. Sort by currency_pair then date
    # ------------------------------------------------------------------
    data = data.sort_values(["currency_pair", "date"]).reset_index(drop=True)

    # ------------------------------------------------------------------
    # 9. Save to pickle for downstream BigQuery loader
    # ------------------------------------------------------------------
    data.to_pickle(output_path)
    logger.info(f"Cleaned data saved to '{output_path}' — final shape: {data.shape}")

    return output_path