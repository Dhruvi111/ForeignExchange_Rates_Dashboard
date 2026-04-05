# FX Analysis Pipeline

A modular Python pipeline that fetches foreign exchange (FX) rate data from the Canadian Border Services Agency (CBSA) API, cleans it, and loads it into Google BigQuery to connect with looker and peform deatiled analysis.

---

## Project Structure

```
fx_analysis/
├── components/
│   ├── data_import.py       # Fetches FX data from the CBSA API
│   ├── data_cleaning.py     # Cleans and transforms raw data
│   ├── data_load.py         # Loads cleaned data into BigQuery
│   └── logger.py            # Centralised logging
├── logs/                    # Auto-generated log files (one per run)
├── venv/                    # Virtual environment (not committed)
├── .env                     # Environment variables (not committed)
└── test.ipynb               # Exploratory notebook
```

---

## Setup

**1. Create and activate virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

**2. Install dependencies**

```bash
pip install requests pandas python-dotenv google-cloud-bigquery google-cloud-bigquery-storage pyarrow
```

**3. Configure `.env`**

```
API_BASE_URL=https://bcd-api-dca-ipa.cbsa-asfc.cloud-nuage.canada.ca/exchange-rate-lambda/exchange-rates
BIGQUERY_PROJECT_ID=your_project_id
```

**4. Authenticate with Google Cloud**

```bash
gcloud init
gcloud auth application-default login
```

---

## Usage

```python
from components.data_import import fetch_exchange_rates
from components.data_cleaning import clean_fx_data
from components.data_load import load_to_bigquery

data     = fetch_exchange_rates(start_date="2025-01-01", end_date="2026-03-06")
pkl_path = clean_fx_data(data)
load_to_bigquery(pkl_path)
```

---

## Notes

- BigQuery dataset (`fx_rates`) and table (`exchange_rates`) are created automatically if they don't exist
- Each run appends data to the existing table (`WRITE_APPEND`)
- All pipeline activity is logged to `logs/pipeline_YYYYMMDD_HHMMSS.log`
- The API fetches data in batches to handle the 1000-row response limit
