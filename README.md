# Mutual Fund NAV Update Pipeline

## Overview
This project simulates a **backend batch data engineering pipeline** used by fintech platforms to refresh **mutual fund NAV (Net Asset Value)** data overnight.

The pipeline ingests NAV data from source systems, processes it using AWS-native services, and publishes analytics-ready data for downstream consumption by APIs or frontend applications.

The focus of this project is **reliable batch processing, clean data lake design, and cost-efficient analytics**, rather than UI or dashboards.

---

## Architecture

![Architecture](https://github.com/SOURAV416/mutual-fund-nav-update-pipeline/blob/9ddd75fa846e4bbc68304ce999900a8332e23830/architecture.png)

### High-Level Flow
- On-prem source systems generate daily NAV snapshots
- Data is ingested into AWS using DMS
- Raw data is stored in Amazon S3
- Nightly ETL jobs process data using AWS Glue
- Processed data is stored in optimized Parquet format
- Amazon Athena enables querying for downstream systems

---

## Architecture Components

### 1. On-Prem Source Systems
Represents upstream relational databases providing daily mutual fund NAV data after market close.

---

### 2. AWS Database Migration Service (DMS)
AWS DMS is used to ingest data from on-prem systems into AWS with minimal impact on source databases.  
The ingestion supports batch and incremental data movement.

---

### 3. Amazon S3 – Raw Zone
Raw NAV data is stored in Amazon S3 without modification.

**Purpose:**
- Source of truth
- Supports reprocessing and backfills
- Preserves original data

**Example path:**
s3://mf-nav-data/raw/nav_date=YYYY-MM-DD/nav_data.csv

---

### 4. Amazon EventBridge (Nightly Schedule)
Amazon EventBridge triggers the ETL pipeline on a **nightly schedule**.

**Why EventBridge:**
- Serverless and managed
- Native AWS integration
- No infrastructure maintenance

---

### 5. AWS Glue (ETL Processing)
AWS Glue runs PySpark-based ETL jobs to process raw NAV data.

**ETL responsibilities:**
- Schema enforcement
- Data type casting
- Deduplication
- Basic data quality checks
- Conversion to Parquet format

---

### 6. Amazon S3 – Processed Zone
Processed NAV data is stored in S3 in **Parquet format**, partitioned by date.

**Benefits:**
- Faster Athena queries
- Reduced query scan cost
- Analytics-ready datasets

**Example path:**
s3://mf-nav-data/processed/nav_date=YYYY-MM-DD/

---

### 7. Amazon Athena (Query Layer)
Amazon Athena is used to query processed data directly from S3.

**Use cases:**
- Fetch latest NAV values
- Historical NAV analysis
- Backend API data access

---

### 8. Downstream Consumers (APIs / Frontend)
Backend APIs or frontend applications query Athena to serve updated NAV values to users.

---

## Technologies Used
- AWS DMS
- Amazon S3
- AWS Glue (PySpark)
- Amazon EventBridge
- Amazon Athena
- Python
- SQL

---

## Setup (High-Level)

1. Create S3 buckets for raw and processed data.
2. Configure AWS DMS to ingest source data into S3 raw zone.
3. Create an AWS Glue job using the provided PySpark script.
4. Set up an EventBridge rule to trigger Glue nightly.
5. Create Athena tables pointing to the processed S3 location.

> Note: This project uses sample/mock data for demonstration purposes.

---

## Usage

- Upload daily NAV data into the S3 raw zone (or simulate ingestion via DMS).
- EventBridge triggers Glue ETL job nightly.
- Processed Parquet data is generated in the processed zone.
- Query latest NAV data using Athena SQL queries.

---

## Key Design Decisions
- **Batch over streaming:** NAV updates are daily, making batch processing optimal.
- **EventBridge over cron:** Fully managed, serverless scheduling.
- **Parquet & partitioning:** Improves performance and reduces cost.
- **Decoupled raw & processed zones:** Enables reprocessing and better governance.

---

## Assumptions
- Sample data is used instead of real mutual fund data.
- Focus is on backend data engineering, not visualization.
- Security and access control are simplified for demonstration.

---

## Future Enhancements
- Add data quality metrics and alerts
- Introduce Step Functions for multi-step orchestration
- Implement cost monitoring and optimization checks

---

## Author
Sourav Nayek
