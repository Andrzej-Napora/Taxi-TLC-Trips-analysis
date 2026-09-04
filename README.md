# NYC TLC Trips Data Pipeline

A data engineering project based on NYC Taxi and Limousine Commission trip records.

The goal is to build an automated pipeline that downloads monthly trip data, loads it into PostgreSQL, applies tested dbt transformations, and prepares datasets for travel time prediction.

# Pipeline

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

# Technology stack

Docker Compose<br>
PostgreSQL and SQL<br>
Python<br>
Requests<br>
Pandas and PyArrow<br>
SQLAlchemy and psycopg2<br>
dbt Core<br>
JupyterLab<br>
Databricks in progress<br>

# Dataset

The project uses NYC TLC Trip Record Data:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

The dataset includes monthly records for:

Yellow Taxi<br>
Green Taxi<br>
For-Hire Vehicles<br>
High Volume For-Hire Vehicles<br>

The Parquet files are not included in the repository, they are downloaded automatically with the 'docker compose up' command.

# Data ingestion

The Python ingestion service automatically:

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

Staging<br>
Standardizes column names and types, applies basic cleaning rules, and performs source-level data quality checks.

Intermediate<br>
Combines compatible trip sources and creates features required for travel time analysis.

Marts<br>
Provides single final table, consisting of all merged taxi category tables prepared for analytics, JupyterLab and machine learning.

# Running the project

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

The first run may take a significant amount of time because the source files contains tens of millions of records.

# Connecting to PostgreSQL

Use the following connection settings in VS Code, DBeaver, pgAdmin or another database client:

Host: `localhost`<br>
Port: `5432`<br>
Database: value of `POSTGRES_DB` from `.env`<br>
Username: value of `POSTGRES_USER` from `.env`<br>
Password: value of `POSTGRES_PASSWORD` from `.env`<br>

# Accessing JupyterLab

JupyterLab is available at: http://localhost:8888

Run
```bash
docker compose logs jupyter
```
search terminal for lines similiar to:
http://localhost:8888/lab?token=ba6a115624519cd432ef3f3b345bf3172f05100ebe27485c
http://127.0.0.1:8888/lab?token=ba6a115624519cd432ef3f3b345bf3172f05100ebe27485c

Copy the generated URL or enter the token at `http://localhost:8888`.

# Stopping the project

To stop and remove the containers while preserving PostgreSQL data:

```bash
docker compose down
```

To remove the containers and PostgreSQL volume:

```bash
docker compose down -v
```

The second command permanently removes the local database.

# Current status

Completed:

Automated monthly Parquet downloads<br>
Memory-efficient batch processing<br>
PostgreSQL bulk ingestion with `COPY FROM STDIN`<br>
Duplicate file protection<br>
Docker Compose pipeline<br>
Layered dbt architecture<br>
Data quality tests<br>
Travel time feature preparation<br>
JupyterLab environment<br>

In progress:

Databricks integration<br>
Apache Spark processing<br>
Delta Lake architecture<br>
Multi-year data processing<br>
Travel time prediction model<br>
Pipeline orchestration and monitoring<br>

# Project purpose

This project was created to develop practical data engineering skills through automated ingestion, large-scale data processing, database design, transformation modeling, data quality testing and reproducible containerized environments.

The local PostgreSQL pipeline serves as a working proof of concept. The next stage focuses on scaling the same workflow with Databricks, Apache Spark and Delta Lake.