# NYC TLC Trips Data Pipeline

A data engineering project based on trip records published by the New York City Taxi and Limousine Commission.

The project contains two versions of the same data pipeline:

1. A local version built with Docker, PostgreSQL and dbt.
2. A Databricks version built with PySpark, Spark SQL, Delta Lake and Lakeflow Pipelines.

Both versions process monthly NYC TLC files and prepare the data for travel time analysis and prediction.

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

Docker Compose starts the services in the correct order. Each service starts after its dependencies are ready.

## Databricks pipeline

NYC TLC Parquet files<br>
→ Python download script<br>
→ source files stored in a Databricks Volume<br>
→ Bronze streaming tables<br>
→ Silver materialized views<br>
→ data quality checks<br>
→ combined Gold dataset<br>
→ travel time prediction<br>

The Databricks pipeline uses the Bronze, Silver and Gold structure.

Bronze<br>
Loads the original Parquet files into Delta tables. Auto Loader keeps track of processed files and loads only new files during later runs.

Silver<br>
Cleans each taxi dataset, standardizes columns and data types, calculates additional values and checks data quality.

Gold<br>
Combines Yellow Taxi, Green Taxi, FHV and High Volume FHV records into one dataset prepared for analysis and machine learning.

# Technology stack

## Local version

Docker Compose<br>
PostgreSQL and SQL<br>
Python<br>
Requests<br>
Pandas and PyArrow<br>
SQLAlchemy and psycopg2<br>
dbt Core<br>
JupyterLab<br>

## Databricks version

Databricks<br>
Apache Spark and PySpark<br>
Spark SQL<br>
Delta Lake<br>
Lakeflow Pipelines<br>
Lakeflow Jobs<br>
Databricks Volumes<br>
Declarative Automation Bundles<br>
Python<br>
SQL<br>
YAML<br>

# Dataset

The project uses the official NYC TLC Trip Record Data:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

The following taxi types are included:

Yellow Taxi<br>
Green Taxi<br>
For-Hire Vehicles<br>
High Volume For-Hire Vehicles<br>

The source Parquet files are not stored in this repository.

The local pipeline downloads them automatically after running:

```bash
docker compose up
```

The Databricks version uses a separate Python script that downloads the selected monthly files into a Databricks Volume.

# Local data ingestion

The local Python ingestion service:

1. generates download URLs for the selected date range<br>
2. downloads only missing Parquet files<br>
3. reads large files in smaller batches with PyArrow<br>
4. keeps column types consistent<br>
5. adds newly detected columns to existing PostgreSQL tables<br>
6. loads batches using PostgreSQL `COPY FROM STDIN`<br>
7. records successfully processed files to prevent duplicate loading<br>

Each taxi type is stored in a separate PostgreSQL table. New monthly files are added to the correct table.

# Local dbt architecture

The dbt project uses three groups of models.

## Staging

The staging models standardize column names and types, perform basic cleaning and run source-level data quality tests.

## Intermediate

The intermediate models prepare compatible taxi datasets for combining and create values required for travel time analysis.

## Marts

The marts provide one final table containing records from all four taxi types.

The final table is prepared for analysis in JupyterLab and for the planned travel time prediction model.

# Databricks architecture

## Source files

The downloaded Parquet files are stored under:

```text
/Volumes/workspace/bronze/raw
```

This location stores the original files before they are loaded into Delta tables.

## Bronze

The Bronze layer uses streaming tables and Auto Loader to process Parquet files.

Each taxi type is stored separately:

```text
workspace.bronze.yellow_trip_records
workspace.bronze.green_trip_records
workspace.bronze.fhv_trip_records
workspace.bronze.fhvhv_trip_records
```

Auto Loader keeps track of processed files. This allows later pipeline runs to load only newly added files.

## Silver

Each taxi type has a separate Spark SQL transformation.

The Silver transformations include:

1. standardizing column names and data types<br>
2. removing records without required values<br>
3. correcting pickup and drop-off time calculations<br>
4. handling daylight saving time changes in New York<br>
5. calculating trip duration<br>
6. detecting negative values<br>
7. checking differences between reported and calculated totals<br>
8. adding missing columns required by the final dataset<br>
9. checking data quality with Lakeflow Expectations<br>

Silver datasets are created as materialized views in the `workspace.silver` schema.

Data quality rules report invalid records without stopping the pipeline or removing all incomplete data.

## Gold

The Gold layer combines all four Silver datasets into one dataset:

```text
workspace.gold.unioned_tables
```

Before combining the datasets, selected columns are converted to common data types.

The final Gold dataset can be used for:

Data analysis<br>
Data visualizations<br>
Travel time prediction<br>
Machine learning experiments<br>

# Databricks workflow

The Databricks workflow contains two tasks:

```text
download_files
      ↓
run_pipeline
```

The first task runs the Python download script.

The second task starts the Lakeflow Pipeline only after the download task finishes successfully.

The Lakeflow Pipeline then creates or updates the Bronze, Silver and Gold datasets in the correct order based on their dependencies.

# Databricks Bundle configuration

The Databricks pipeline and Job are described by YAML files stored in this repository.

The main Bundle configuration file is:

```text
databricks/databricks.yml
```

The pipeline and Job resources are defined in:

```text
databricks/resources/pipeline.yml
databricks/resources/job.yml
```

The configuration includes:

Pipeline source files<br>
Job tasks and their execution order<br>
Databricks catalog and default schema<br>
Serverless compute settings<br>
Photon configuration<br>
Development mode<br>
New York time zone configuration<br>

The pipeline uses:

```yaml
spark.sql.session.timeZone: America/New_York
```

This setting ensures that timestamp values are interpreted using the New York time zone.

# Databricks project structure

```text
databricks/
├── databricks.yml
├── resources/
│   ├── pipeline.yml
│   └── job.yml
└── nyc_tlc_pipeline/
    ├── files_download/
    ├── bronze_transformations/
    ├── silver_transformations/
    └── gold_transformations/
```

# Deploying the Databricks pipeline

The Databricks version requires:

Databricks workspace access<br>
Databricks CLI<br>
An existing catalog and schemas<br>
A Volume for the source Parquet files<br>
Permissions to create and update pipeline datasets<br>

Open a terminal in the `databricks` directory:

```bash
cd databricks
```

Validate the Bundle configuration:

```bash
databricks bundle validate -t dev
```

Deploy the pipeline and Job:

```bash
databricks bundle deploy -t dev
```

Run the complete workflow:

```bash
databricks bundle run nyc_tlc_job -t dev
```

These commands perform three separate operations:

```text
validate → checks the configuration
deploy   → creates or updates the Databricks resources
run      → starts the complete workflow
```

The workflow can also be started from the Databricks `Jobs & Pipelines` page after it has been deployed.

The Bundle configuration allows the pipeline, Job and their settings to be stored in GitHub and deployed to another Databricks workspace.

The source data, existing tables, permissions and user credentials are not stored in the repository. They must be prepared separately in the target workspace.

# Running the local pipeline

Install and start Docker Desktop.

Create a `.env` file based on `.env.example`:

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
```

Do not commit the `.env` file to GitHub.

Start the pipeline from the project directory:

```bash
docker compose up
```

Docker Compose will:

1. start PostgreSQL<br>
2. wait until the database is ready<br>
3. download and load missing NYC TLC files<br>
4. build and test the dbt models<br>
5. start JupyterLab after the previous steps finish successfully<br>

The first run can take a long time because the source files contain tens of millions of records.

# Connecting to PostgreSQL

Use the following settings in VS Code, DBeaver, pgAdmin or another database client:

Host: `localhost`<br>
Port: `5432`<br>
Database: value of `POSTGRES_DB` from `.env`<br>
Username: value of `POSTGRES_USER` from `.env`<br>
Password: value of `POSTGRES_PASSWORD` from `.env`<br>

# Accessing JupyterLab

JupyterLab is available at:

```text
http://localhost:8888
```

To find the access token, run:

```bash
docker compose logs jupyter
```

Look for a URL similar to:

```text
http://127.0.0.1:8888/lab?token=generated_token
```

Copy the complete URL and open it in a browser.

# Stopping the local pipeline

To stop and remove the Docker containers while keeping the PostgreSQL data:

```bash
docker compose down
```

To remove the containers and the PostgreSQL data:

```bash
docker compose down -v
```

The second command permanently removes the local database.

# Current status

## Completed local pipeline

Automated monthly Parquet downloads<br>
Memory-efficient batch processing<br>
PostgreSQL loading with `COPY FROM STDIN`<br>
Protection against loading the same file more than once<br>
Docker Compose pipeline<br>
dbt staging, intermediate and marts models<br>
dbt data quality tests<br>
Travel time feature preparation<br>
JupyterLab environment<br>

## Completed Databricks pipeline

Databricks schemas created<br>
Volume for source Parquet files configured<br>
Python download script adapted to Databricks<br>
Eight months of source Parquet files downloaded<br>
Initial data exploration with PySpark<br>
Bronze streaming tables created with Auto Loader<br>
Separate Silver transformations created for each taxi type<br>
Lakeflow data quality rules added<br>
Gold dataset combining all taxi types created<br>
New York time zone added to the pipeline configuration<br>
Declarative Automation Bundle created and validated<br>
Lakeflow Job created for workflow orchestration<br>
Download task connected to the Lakeflow Pipeline<br>
Pipeline and Job successfully deployed from YAML configuration<br>
Complete Databricks workflow successfully executed<br>

## In progress

Reviewing data quality results<br>
Adding PySpark tests for the Gold dataset<br>
Processing a larger date range<br>
Improving pipeline monitoring<br>
Travel time prediction model<br>
Additional setup instructions for a new Databricks workspace<br>

# Project purpose

This project was created to develop practical data engineering skills.

The local version focuses on Docker, PostgreSQL, Python and dbt. It shows how the complete pipeline can run on one computer.

The Databricks version uses the same source data and similar transformation rules, but processes the data with Apache Spark, Delta Lake and Lakeflow Pipelines.

Building both versions makes it possible to compare a local data pipeline with a cloud data platform and understand how the same process can be built with different tools.