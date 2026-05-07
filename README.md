# FX Analysis Dashboard

## Project Overview

This project builds a production-ready data pipeline for monitoring foreign exchange rates against the Canadian Dollar (CAD). It covers the full data engineering lifecycle involving an end-to-end data pipeline that ingests foreign exchange rate data from the Canadian Border Services Agency (CBSA) API, transforms it, loads it into Google BigQuery, and visualizes it through a live Looker Studio dashboard — fully automated with daily scheduling via Google Cloud.

[View Live Dashboard](https://datastudio.google.com/s/uxCmk-JEY9w)**
---


## 🎯 Key Objectives

- Ingest daily FX rate data from the CBSA public API with dynamic batch handling
- Clean, validate, and transform raw data into an analytics-ready format
- Load structured data into Google BigQuery with automatic schema creation
- Compute analytical metrics using BigQuery views
- Visualize trends, volatility, and currency comparisons in Looker Studio
- Automate the full pipeline to run daily using Google Cloud Run Jobs and Cloud Scheduler

---

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.11 |
| Data Processing | Pandas, PyArrow |
| API Ingestion | Requests |
| Cloud Platform | Google Cloud Platform (GCP) |
| Data Warehouse | Google BigQuery |
| Containerization | Docker |
| Container Registry | Google Artifact Registry |
| Pipeline Execution | Google Cloud Run Jobs |
| Scheduling | Google Cloud Scheduler |
| Visualization | Looker Studio |
| Version Control | Git / GitHub |

---

## Skills Demonstrated

- **Data Engineering** — end-to-end pipeline design with modular, production-ready Python code
- **API Integration** — dynamic batch ingestion with adaptive rate limiting to handle API row caps
- **Data Cleaning & Transformation** — null handling, type casting, column normalization, feature engineering
- **Cloud Infrastructure** — GCP service setup, IAM roles, service accounts, Artifact Registry
- **Containerization** — Dockerizing a Python pipeline for cloud deployment
- **Pipeline Automation** — scheduling daily runs using Cloud Run Jobs + Cloud Scheduler
- **Analytical SQL** — BigQuery window functions (`LAG`, `STDDEV`, `PARTITION BY`) for computed metrics
- **Data Visualization** — Looker Studio dashboard with interactive filters and time series analysis
---

## Project Stages

### Stage 1 — Data Ingestion
- Connected to the CBSA FX rates public API
- Implemented adaptive batch fetching to handle the 1000-row API response limit
- Returns a complete `pd.DataFrame` for any date range

### Stage 2 — Data Cleaning & Transformation
- Renamed verbose API column names to snake_case
- Cast data types, extracted date column, dropped unused columns
- Added `currency_pair` feature (e.g. `USD/CAD`)
- Null/missing value detection with automated row dropping and logging
- Output saved as a `.pkl` file for downstream loading

### Stage 3 — BigQuery Loading
- Auto-creates dataset and table if they don't exist
- Appends new data on each run
- All activity logged to timestamped log files

### Stage 4 — Analytical Views
- Created a BigQuery view on top of the raw table computing:
  - Daily % change using `LAG()`
  - 30-day rolling standard deviation using `STDDEV()` window function

### Stage 5 — Dashboard (Looker Studio)
- **Currencies Tracked** — scorecard showing total number of currency pairs monitored
- **Latest Rates Table** — most recent exchange rates with daily % change for major currencies
- **% Change Time Series** — interactive chart comparing daily % change across multiple currencies and time periods
- **Moving Average Time Series** — interactive trend chart comparing smoothed rates across multiple currencies and time periods

### Stage 6 — Automation
- Containerized the pipeline using Docker and pushed to Google Artifact Registry
- Deployed as a Cloud Run Job and scheduled daily at 12 AM UTC via Cloud Scheduler
- Pipeline automatically fetches, cleans, and appends yesterday's data to BigQuery daily

---

## Project Structure

```
fx_analysis/
├── components/          # Python modules (ingestion, cleaning, loading, logging)
├── logs/                # Auto-generated timestamped log files
├── venv/                # Virtual environment (not committed)
├── .env                 # Environment variables (not committed)
├── Dockerfile           # Container definition for Cloud Run
├── requirements.txt     # Python dependencies
├── main.py              # Pipeline entry point
└── test.ipynb           # Exploratory analysis notebook
```

---

## Setup & Usage

**1. Clone the repo and activate virtual environment**
```bash
git clone https://github.com/yourusername/fx_analysis.git
cd fx_analysis
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Configure `.env`**
```
API_BASE_URL=https://bcd-api-dca-ipa.cbsa-asfc.cloud-nuage.canada.ca/exchange-rate-lambda/exchange-rates
BIGQUERY_PROJECT_ID=your_project_id
```

**3. Authenticate with GCP**
```bash
gcloud auth application-default login
```

**4. Run the pipeline**
```bash
python main.py
```
