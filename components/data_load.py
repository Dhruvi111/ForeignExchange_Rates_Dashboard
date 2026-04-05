"""
data_load.py
--------------
Loads cleaned FX exchange rate data from a pickle file into BigQuery.
Creates the dataset and table if they do not already exist.
"""

import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

from google.cloud import bigquery
from google.api_core.exceptions import Conflict

from components.logger import get_logger

# load_dotenv()

logger = get_logger(__name__)

# ------------------------------------------------------------------
# Constants — dataset and table are created by code, not config
# ------------------------------------------------------------------
DATASET_ID = "fx_rates"
TABLE_ID   = "exchange_rates"

# ------------------------------------------------------------------
# BigQuery schema — matches the cleaned DataFrame columns
# ------------------------------------------------------------------
SCHEMA = [
    bigquery.SchemaField("exchangerateid",      "INTEGER"),
    bigquery.SchemaField("rate",                "FLOAT"),
    bigquery.SchemaField("effective_timestamp", "TIMESTAMP"),
    bigquery.SchemaField("source",              "STRING"),
    bigquery.SchemaField("from_currency",       "STRING"),
    bigquery.SchemaField("to_currency",         "STRING"),
    bigquery.SchemaField("date",                "DATE"),
    bigquery.SchemaField("currency_pair",       "STRING"),
]


def load_to_bigquery(pkl_path: str) -> None:
    """
    Load cleaned FX data from a pickle file into BigQuery.
    Creates the dataset and table if they do not already exist.

    Parameters
    ----------
    pkl_path : str
        Path to the cleaned pickle file produced by clean_fx_data().
    """

    # ------------------------------------------------------------------
    # 1. Load project ID from .env
    # ------------------------------------------------------------------
    project_id = os.getenv("BIGQUERY_PROJECT_ID")
    if not project_id:
        logger.error("BIGQUERY_PROJECT_ID is not set. Please add it to your .env file.")
        raise ValueError("BIGQUERY_PROJECT_ID is not set.")

    logger.info(f"Starting BigQuery load — project: {project_id}")

    # ------------------------------------------------------------------
    # 2. Initialise BigQuery client
    # ------------------------------------------------------------------
    client = bigquery.Client(project=project_id)
    logger.info("BigQuery client initialised.")

    # ------------------------------------------------------------------
    # 3. Create dataset if it doesn't exist
    # ------------------------------------------------------------------
    dataset_ref = bigquery.Dataset(f"{project_id}.{DATASET_ID}")
    dataset_ref.location = "US"

    try:
        client.create_dataset(dataset_ref)
        logger.info(f"Dataset '{DATASET_ID}' created.")
    except Conflict:
        logger.info(f"Dataset '{DATASET_ID}' already exists — skipping creation.")

    # ------------------------------------------------------------------
    # 4. Create table if it doesn't exist
    # ------------------------------------------------------------------
    table_ref = bigquery.Table(f"{project_id}.{DATASET_ID}.{TABLE_ID}", schema=SCHEMA)

    try:
        client.create_table(table_ref)
        logger.info(f"Table '{TABLE_ID}' created.")
    except Conflict:
        logger.info(f"Table '{TABLE_ID}' already exists — skipping creation.")

    # ------------------------------------------------------------------
    # 5. Read pickle file
    # ------------------------------------------------------------------
    logger.info(f"Reading pickle file from '{pkl_path}'...")
    df = pd.read_pickle(pkl_path)
    logger.info(f"Loaded {len(df)} rows from pickle.")

    # ------------------------------------------------------------------
    # 6. Load data into BigQuery
    # ------------------------------------------------------------------
    job_config = bigquery.LoadJobConfig(
        schema=SCHEMA,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,  # append to existing data
    )

    destination = f"{project_id}.{DATASET_ID}.{TABLE_ID}"
    logger.info(f"Loading data into '{destination}'...")

    job = client.load_table_from_dataframe(df, destination, job_config=job_config)
    job.result()  # wait for job to complete

    # ------------------------------------------------------------------
    # 7. Confirm rows loaded
    # ------------------------------------------------------------------
    table = client.get_table(destination)
    logger.info(f"Load complete. Total rows now in table: {table.num_rows}")