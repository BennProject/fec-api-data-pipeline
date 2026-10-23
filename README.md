# FEC API Data Pipeline

## Project Overview

This project builds a data pipeline that ingests 2026 U.S. House and Senate candidate data from the OpenFEC API, stores the collected data in Amazon S3, transforms it into Parquet format, and queries the processed data using Amazon Athena.

The project was built as part of my AWS Data Engineer learning path to practice working with REST API ingestion, Python, Amazon S3, Parquet, the AWS Glue Data Catalog, and Amazon Athena.

## Pipeline Architecture

OpenFEC API → Python → Amazon S3 Raw JSON → Python Transformation → Amazon S3 Curated Parquet → AWS Glue Data Catalog → Amazon Athena

## Technologies Used

- Python
- Requests
- Boto3
- pandas
- PyArrow
- Amazon S3
- AWS IAM
- AWS Glue Data Catalog
- Amazon Athena
- OpenFEC API

## Data Ingestion

The ingestion script connects to the OpenFEC API and retrieves active 2026 U.S. House and Senate candidate records.

The API request uses pagination to collect all records matching the 2026 House and Senate candidate filters.

During the completed pipeline run:

- 43 API pages were processed
- 4,292 candidate records were collected
- The collected record count was compared with the API-reported total
- The counts matched successfully

The collected API results are stored as JSON in the raw S3 data layer.

## Data Transformation

A separate Python script reads the raw JSON data from Amazon S3 and converts the dataset into an analytics-ready Parquet file.

The curated dataset contains 18 selected fields, including:

- Candidate ID and name
- Office and state
- District
- Party
- Candidate status
- Incumbent/challenger classification
- Fundraising-related flags
- Filing dates
- Election years

The transformation uses pandas and PyArrow and writes the resulting Parquet file to a separate curated S3 location.

## Data Storage

The project separates the data into two S3 layers:

**Raw Layer**

Stores the collected API results as JSON.

**Curated Layer**

Stores the transformed dataset as Parquet for analytical queries.

## Data Catalog and Querying

An external table was created in Amazon Athena for the curated Parquet dataset.

The table metadata is registered in the AWS Glue Data Catalog.

A validation query confirmed that all 4,292 records were preserved through the pipeline.

Example validation query:

```sql
SELECT COUNT(*)
FROM fec_pipeline.candidates_curated;
```

Result:

```text
4292
```

Additional Athena queries were used to analyze fundraising-related flags and incumbent/challenger classifications.

## Validation

The pipeline was validated at multiple stages:

- API-reported record count: 4,292
- Python records collected: 4,292
- Rows transformed to Parquet: 4,292
- Athena row count: 4,292

This confirmed that the full dataset was preserved through ingestion, transformation, storage, and querying.

## Security

The OpenFEC API key is read from an environment variable rather than being stored directly in the Python code.

AWS credentials are also not stored in the repository.

## Project Files

- `fec_pipeline.py` — Retrieves OpenFEC candidate data and uploads the raw JSON dataset to Amazon S3
- `transform_candidates.py` — Reads raw S3 data, selects curated fields, converts the dataset to Parquet, and uploads the processed file to S3
- `FEC_API_DataPipeline_Report.pdf` — Project documentation and learning summary
- Project screenshots — Evidence of ingestion, transformation, S3 storage, and Athena validation

## Key Skills Practiced

- REST API ingestion
- API authentication
- Pagination
- HTTP response handling
- Python data processing
- Programmatic S3 access with Boto3
- Raw and curated data-layer design
- JSON-to-Parquet transformation
- AWS Glue Data Catalog integration
- Amazon Athena SQL queries
- Data validation across pipeline stages

## Project Scope

This project represents a completed learning and portfolio pipeline built from a snapshot of OpenFEC candidate data collected on October 8, 2026.

It is intended to demonstrate the core flow of ingesting, transforming, storing, cataloging, and querying data using Python and AWS services.
