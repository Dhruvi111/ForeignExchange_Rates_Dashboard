# Foreign Exchange Monitoring Dashboard (CAD-Based)

## Project Overview
This project builds a live foreign exchange (FX) monitoring dashboard that tracks daily exchange rates relative to the Canadian Dollar (CAD). The system ingests exchange rate data from the official API provided by the Bank of Canada, processes and transforms the data using a Python-based ETL pipeline, stores the cleaned data in Google BigQuery, and visualizes insights through an automated Looker Studio dashboard with daily refresh. The dataset includes historical exchange rate data from January 2024 to present, along with incremental daily updates to ensure the dashboard remains current. The dashboard provides near real-time visibility into currency trends, percentage changes, and volatility patterns.

---

## Key Objectives

- Build an automated ETL pipeline for daily FX data ingestion  
- Ingest historical data from **Jan 2024 – Present**  
- Implement incremental daily updates  
- Store structured exchange rate data in a cloud warehouse  
- Create a live dashboard with automated refresh  
- Enable monitoring of:
  - Daily exchange rate values (CAD base)
  - Daily % change
  - Rolling averages
  - Volatility indicators  
- Showcase a production-grade analytics workflow with version control and documentation  

---

## Tech Stack

- Data Ingestion & Processing: Python, Pandas, Requests, Logging  

- Data Storage: Google BigQuery  

- Visualization: Looker Studio (live dashboard with scheduled refresh)

- Automation: Google Cloud Functions, Cloud Scheduler  

---

## System Architecture

Bank of Canada API  
→ Python ETL (Historical + Incremental Load)  
→ Data Cleaning & Feature Engineering  
→ BigQuery 
→ Looker Studio 
→ Automated Daily Refresh  

---

## Dashboard Features

- Multi-currency selection  
- Daily exchange rate tracking (CAD base)  
- Historical trend analysis 
- Daily percentage change  
- 7-day / 30-day moving averages  
- Rolling volatility  
- Interactive date filters and visuals  

---

## Project Stages

### Stage 1 – Data Source Setup
- Understand Bank of Canada API structure and parameters  
- Configure API requests for historical data retrieval  
- Validate API responses and data format  
- Ensure access to historical data from Jan 2024 – Present  
- Handle missing dates (weekends/holidays) and null values  

---

### Stage 2 – Historical Backfill
- Fetch exchange rate data from Jan 2024 to current date  
- Clean and standardize fields  
- Validate completeness and consistency  
- Load initial dataset into BigQuery  

---

### Stage 3 – ETL Development
- Build modular Python pipeline  
- Implement data validation and error handling  
- Handle missing/null values  
- Engineer derived metrics:
  - Daily % change  
  - Moving averages  
  - Volatility  
- Implement incremental loading logic  

---

### Stage 4 – Data Warehouse Setup
- Create BigQuery dataset  
- Define schema and table structure  
- Partition table by date  
- Optimize query performance  

---

### Stage 5 – Automation
- Deploy ETL using Google Cloud Functions  
- Schedule daily execution using Cloud Scheduler  
- Configure logging and monitoring  
- Ensure idempotent pipeline runs  

---

### Stage 6 – Dashboard Development
- Connect BigQuery to Looker Studio  
- Design KPI metrics  
- Create trend charts and filters  
- Optimize dashboard performance  
- Configure automatic data refresh  

---

### Stage 7 – Documentation & Deployment
- Maintain README and architecture documentation  
- Implement `.gitignore`  
- Organize repository structure  
- Document setup and deployment steps  

---

## Task List

### Data Engineering
- [ ] Configure API connection  
- [ ] Fetch historical data 
- [ ] Build incremental daily ingestion  
- [ ] Implement error handling  
- [ ] Add logging  
- [ ] Create BigQuery tables  
- [ ] Enable partitioning & clustering  

---

### Analytics
- [ ] Calculate daily % change  
- [ ] Add moving averages  
- [ ] Compute rolling volatility  

---

### Dashboard
- [ ] Create currency selector  
- [ ] Add trend visualizations  
- [ ] Add KPI summary cards  
- [ ] Configure scheduled refresh  

---

### DevOps & Documentation
- [ ] Set up GitHub repository  
- [ ] Add `.gitignore`  
- [ ] Write setup instructions  
- [ ] Add architecture diagram  

---

## 🔄 Automation Workflow

Cloud Scheduler (Daily Trigger)  
→ Cloud Function executes ETL  
→ New data appended to BigQuery  
→ Looker Studio reflects updated data automatically  

---
