# NYC TLC Trips Data Pipeline

A data engineering project based on trip records published by the New York City Taxi and Limousine Commission.

The repository contains two implementations of the same pipeline:

1. A local pipeline built with Docker, PostgreSQL and dbt.
2. A Databricks pipeline built with PySpark, Spark SQL, Delta Lake and Lakeflow Pipelines.

Both implementations process monthly NYC TLC Parquet files and create a unified dataset for analysis and future travel time prediction.

## Pipeline overview

### Local pipeline

```text
NYC TLC Parquet files
        ↓
Python ingestion with PyArrow
        ↓
PostgreSQL raw tables
        ↓
dbt staging and intermediate models
        ↓
dbt marts
        ↓
JupyterLab
```

Docker Compose starts PostgreSQL, loads missing source files, builds the dbt models and starts JupyterLab.

### Databricks pipeline

```text
NYC TLC Parquet files
        ↓
Python download task
        ↓
Databricks Volume
        ↓
Bronze streaming tables
        ↓
Silver materialized views
        ↓
Gold unified dataset
        ↓
Integration tests
```

The Databricks implementation follows the Bronze, Silver and Gold architecture.

- Bronze loads source files into Delta streaming tables with Auto Loader.
- Silver cleans and standardizes each taxi dataset and applies data quality checks.
- Gold combines all taxi types into one dataset prepared for analysis and machine learning.

## Technology stack

### Local pipeline

- Docker Compose
- PostgreSQL and SQL
- Python
- Requests
- Pandas and PyArrow
- SQLAlchemy and psycopg2
- dbt Core
- JupyterLab

### Databricks pipeline

- Databricks
- Apache Spark and PySpark
- Spark SQL
- Delta Lake
- Lakeflow Pipelines
- Lakeflow Jobs
- Databricks Volumes
- Declarative Automation Bundles
- Python, SQL and YAML

### Testing and CI

- pytest
- requests-mock
- Ruff
- yamllint
- Python compileall
- GitHub Actions

## Dataset

The project uses the official NYC TLC Trip Record Data:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Included taxi types:

- Yellow Taxi
- Green Taxi
- For-Hire Vehicles
- High Volume For-Hire Vehicles

Source Parquet files are not stored in this repository. Both pipeline versions download missing files automatically.

## Local pipeline

The local ingestion service:

1. Generates URLs for the selected monthly range.
2. Downloads only missing files.
3. Processes large Parquet files in smaller PyArrow batches.
4. Loads data into PostgreSQL with `COPY FROM STDIN`.
5. Tracks completed files to prevent duplicate loading.

Each taxi type is stored in a separate PostgreSQL table.

The dbt project contains:

- staging models for cleaning and standardization,
- intermediate models for compatible schemas and calculated values,
- marts combining all taxi types into one final dataset.

## Databricks architecture

### Source files

Source files are stored in a Unity Catalog Volume. The default development location is:

```text
/Volumes/workspace/bronze/raw
```

The location can be changed through Bundle variables.

### Bronze

Auto Loader processes source Parquet files and tracks previously loaded data.

Each taxi type is stored in a separate streaming table.

### Silver

Separate Spark SQL transformations:

- standardize column names and data types,
- remove records without required values,
- handle New York daylight saving time,
- calculate trip duration,
- identify invalid values,
- apply Lakeflow Expectations,
- prepare compatible schemas for the Gold layer.

### Gold

The Gold layer combines all four taxi datasets into:

```text
workspace.gold.unioned_tables
```

The result is prepared for data analysis, visualization and travel time prediction.

## Databricks workflow

The Lakeflow Job contains three dependent tasks:

```text
download_files
      ↓
run_pipeline
      ↓
test_gold
```

`download_files` calculates the required monthly range and downloads only missing source files.

`run_pipeline` starts the Lakeflow Pipeline after the download task succeeds.

`test_gold` runs integration checks against the completed Gold dataset, including:

- record count consistency,
- expected taxi type values,
- schema consistency,
- pickup and drop-off time consistency,
- required value completeness,
- valid NYC TLC location identifiers.

These checks require Spark and existing tables, so they run inside Databricks.

## Unit tests

Local tests are stored in:

```text
databricks/nyc_tlc_pipeline/tests/
```

The tests cover Python functions that do not require a running Spark session, including:

- monthly date range generation,
- successful HTTP responses,
- existing file detection,
- HTTP and connection errors,
- generated file names and URLs,
- binary file output.

HTTP calls are replaced with `requests-mock`, so tests do not connect to the NYC TLC server.

Test files are written to temporary pytest directories and removed after the tests finish.

Run the tests:

```bash
python -m pytest ./databricks/nyc_tlc_pipeline/tests
```

## Databricks Bundle

The main Bundle configuration is stored in:

```text
databricks/databricks.yml
```

Resource definitions are stored in:

```text
databricks/resources/job.yml
databricks/resources/pipeline.yml
```

The Bundle defines:

- Lakeflow Pipeline sources,
- Lakeflow Job tasks and dependencies,
- catalogs and schemas,
- serverless compute and Photon,
- environment variables,
- development and production targets,
- time zones and the production schedule.

### Deployment targets

The `dev` target:

- uses development mode,
- uses schemas with the `_dev` suffix,
- keeps the schedule paused,
- uses a deployment path associated with the current user.

The `prod` target:

- uses production mode,
- uses production schemas,
- enables the schedule,
- uses a stable shared deployment path.

Resource names contain the selected target:

```text
nyc_tlc_job_dev
nyc_tlc_job_prod
nyc_tlc_project_dev
nyc_tlc_project_prod
```

### Time zones

Taxi timestamps are processed with:

```yaml
spark.sql.session.timeZone: America/New_York
```

The production schedule uses:

```text
Europe/Warsaw
```

The source data time zone and job schedule time zone are configured separately.

## Databricks project structure

```text
databricks/
├── databricks.yml
├── resources/
│   ├── job.yml
│   └── pipeline.yml
└── nyc_tlc_pipeline/
    ├── files_download/
    ├── bronze_transformations/
    ├── silver_transformations/
    ├── gold_transformations/
    └── tests/
```

## Continuous integration

GitHub Actions runs CI for every pull request targeting `main`.

The workflow is defined in:

```text
.github/workflows/ci.yml
```

CI contains two independent jobs.

The code quality job runs:

- yamllint for YAML files,
- compileall for Python syntax,
- Ruff for Python code quality.

The test job prepares a clean Python environment and runs pytest.

The `main` branch is protected. Changes must be submitted through a pull request, and all required CI checks must pass before merging.

## Continuous delivery

Production deployment is performed manually after successful CI and merge into `main`.

Databricks Free Edition does not provide the account-level service principal configuration required for unattended deployment through GitHub Actions.

The complete process is:

```text
Feature branch
      ↓
Pull request
      ↓
GitHub Actions CI
      ↓
Merge into main
      ↓
Manual Bundle validation
      ↓
Manual Bundle deployment
      ↓
Automatic execution through the Databricks schedule
```

This keeps code validation automated without storing long-lived Databricks credentials in GitHub.

## Deploying to Databricks

Open a terminal in the Bundle directory:

```bash
cd databricks
```

Validate the development target:

```bash
databricks bundle validate -t dev
```

Deploy and run the development target:

```bash
databricks bundle deploy -t dev
databricks bundle run nyc_tlc_job -t dev
```

Validate and deploy production:

```bash
databricks bundle validate -t prod
databricks bundle deploy -t prod
```

The production deployment does not run the Job immediately. Databricks starts it according to the schedule defined in the Bundle.

The workspace catalog, schemas, Volume, permissions and user credentials must be configured separately. They are not stored in this repository.

## Running the local pipeline

Create a `.env` file based on `.env.example`:

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
```

Do not commit `.env`.

Start the pipeline:

```bash
docker compose up
```

JupyterLab is available at:

```text
http://localhost:8888
```

Find the generated access token with:

```bash
docker compose logs jupyter
```

Stop the containers while keeping PostgreSQL data:

```bash
docker compose down
```

Remove the containers and PostgreSQL data:

```bash
docker compose down -v
```

The second command permanently removes the local database volume.

## Current status

Completed:

- automated monthly data ingestion,
- PostgreSQL loading with `COPY FROM STDIN`,
- Docker Compose orchestration,
- dbt staging, intermediate and marts models,
- Bronze streaming tables with Auto Loader,
- Silver Spark SQL transformations,
- Lakeflow Expectations,
- unified Gold dataset,
- Declarative Automation Bundle,
- separate `dev` and `prod` targets,
- production schedule,
- Lakeflow Job orchestration,
- Gold integration checks,
- local unit tests with mocked HTTP requests,
- automated GitHub Actions CI,
- protected `main` branch,
- manual production deployment.

Planned:

- expanded test coverage,
- improved pipeline monitoring,
- larger date range processing,
- travel time prediction model,
- setup instructions for another Databricks workspace.

## Project purpose

This project was created to develop practical data engineering skills.

The local implementation demonstrates a complete pipeline built with Docker, PostgreSQL, Python and dbt.

The Databricks implementation processes the same data with Apache Spark, Delta Lake, Lakeflow Pipelines and Declarative Automation Bundles.

Maintaining both implementations makes it possible to compare a local data stack with a cloud data platform.