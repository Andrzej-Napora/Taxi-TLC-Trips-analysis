# NYC TLC Trips Data Pipeline

A data engineering project based on NYC Taxi and Limousine Commission trip records.

The goal is to build an automated pipeline that downloads monthly trip data, loads it into PostgreSQL, applies tested dbt transformations, and prepares datasets for travel time prediction.

# Pipeline

## Local pipeline

NYC TLC Parquet files<br>
→ automated Python ingestion<br>
→ batch processing with PyArrow<br>
→ PostgreSQL raw tables<br>
→ dbt staging models<br>
→ dbt intermediate models<br>
→ dbt marts<br>
→ JupyterLab<br>
→ travel time prediction<br>

Docker Compose controls the execution order and starts each service after its dependencies complete successfully.

## Databricks pipeline

NYC TLC Parquet files<br>
→ Python ingestion into a Unity Catalog Volume<br>
→ Bronze Delta tables<br>
→ Silver validation and cleaning<br>
→ Gold analytical models<br>
→ data quality tests<br>
→ travel time prediction<br>

The Databricks pipeline is currently under development. It is intended to process the same source data using PySpark, Delta Lake and the medallion architecture.

# Technology stack

Docker Compose<br>
PostgreSQL and SQL<br>
Python<br>
Requests<br>
Pandas and PyArrow<br>
SQLAlchemy and psycopg2<br>
dbt Core<br>
JupyterLab<br>
Databricks<br>
Apache Spark and PySpark<br>
Unity Catalog and Volumes<br>
Delta Lake in progress<br>

# Dataset

The project uses NYC TLC Trip Record Data:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

The dataset includes monthly records for:

Yellow Taxi<br>
Green Taxi<br>
For-Hire Vehicles<br>
High Volume For-Hire Vehicles<br>

The Parquet files are not included in the repository. They are downloaded automatically with the `docker compose up` command for the local pipeline.

The Databricks implementation uses a separate Python ingestion script that downloads selected monthly files directly into a Unity Catalog Volume.

# Data ingestion

The local Python ingestion service automatically:

1. generates download URLs for a selected date range<br>
2. downloads only missing Parquet files<br>
3. reads large files in batches with PyArrow<br>
4. preserves and standardizes column types<br>
5. adds newly detected columns to existing PostgreSQL tables<br>
6. loads batches using PostgreSQL `COPY FROM STDIN`<br>
7. records successfully processed files to prevent duplicate ingestion<br>

Each taxi category is stored in a separate raw table. New monthly files are appended to their corresponding tables.

# dbt architecture

The dbt project uses three transformation layers:

## Staging

Standardizes column names and types, applies basic cleaning rules, and performs source-level data quality checks.

## Intermediate

Combines compatible trip sources and creates features required for travel time analysis.

## Marts

Provides a single final table consisting of all merged taxi category tables prepared for analytics, JupyterLab and machine learning.

# Databricks pipeline

Development of a separate Databricks implementation has started.

The current implementation includes:

1. Unity Catalog schemas for the medallion architecture<br>
2. a Unity Catalog Volume used as the raw data landing area<br>
3. a Python ingestion script for downloading selected monthly files directly into the Volume<br>
4. eight months of NYC TLC data from August 2024 through March 2025<br>
5. initial data inspection and schema validation with PySpark<br>
6. development of incremental ingestion into Bronze tables<br>
7. cleaning, format standarizing, feature engineering with Silver tables<br>
8. unifying silver tables for one Gold table, ready for analytics and machine learning


# Running the local project

Install and start Docker Desktop.

Create a `.env` file based on `.env.example` and provide PostgreSQL credentials:

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
```

Start the pipeline from the project directory:

```bash
docker compose up
```

Docker Compose will automatically:

1. start PostgreSQL<br>
2. wait until the database is healthy<br>
3. download and load missing NYC TLC files<br>
4. build and test the dbt models<br>
5. start JupyterLab after successful completion<br>

The first run may take a significant amount of time because the source files contain tens of millions of records.

# Connecting to PostgreSQL

Use the following connection settings in VS Code, DBeaver, pgAdmin or another database client:

Host: `localhost`<br>
Port: `5432`<br>
Database: value of `POSTGRES_DB` from `.env`<br>
Username: value of `POSTGRES_USER` from `.env`<br>
Password: value of `POSTGRES_PASSWORD` from `.env`<br>

# Accessing JupyterLab

JupyterLab is available at:

http://localhost:8888

Run:

```bash
docker compose logs jupyter
```

Search the terminal output for lines similar to:

```text
http://localhost:8888/lab?token=generated_token
http://127.0.0.1:8888/lab?token=generated_token
```

Copy one of the generated URLs or enter the token at:

http://localhost:8888

# Stopping the project

To stop and remove the containers while preserving PostgreSQL data:

```bash
docker compose down
```

To remove the containers and the PostgreSQL volume:

```bash
docker compose down -v
```

The second command permanently removes the local database.

# Current status

## Completed local pipeline

Automated monthly Parquet downloads<br>
Memory-efficient batch processing<br>
PostgreSQL bulk ingestion with `COPY FROM STDIN`<br>
Duplicate file protection<br>
Docker Compose pipeline<br>
Layered dbt architecture<br>
Data quality tests<br>
Travel time feature preparation<br>
JupyterLab environment<br>

## Databricks development completed so far

Unity Catalog schemas created<br>
Raw Unity Catalog Volume configured<br>
Python download script adapted to Databricks Volumes<br>
Eight months of source Parquet files downloaded<br>
Initial PySpark data exploration<br>
Initial Bronze ingestion development<br>
Silver data cleaning and validation<br>
Gold analytical models<br>

## In progress

Incremental Bronze ingestion<br>
Delta Lake medallion architecture<br>
Automated data quality checks in Databricks<br>
Multi-year data processing<br>
Travel time prediction model<br>
Databricks workflow orchestration and monitoring<br>
GitHub integration and reproducible Databricks deployment<br>

# Project purpose

This project was created to develop practical data engineering skills through automated ingestion, large-scale data processing, database design, transformation modeling, data quality testing and reproducible containerized environments.

The local PostgreSQL and dbt pipeline serves as a working proof of concept. A separate Databricks implementation is now under development to process the same source data using PySpark, Unity Catalog, Delta Lake and the Bronze, Silver and Gold medallion architecture.