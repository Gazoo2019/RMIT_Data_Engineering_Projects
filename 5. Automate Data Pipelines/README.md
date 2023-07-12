# Sparkify Data Pipeline
*Automating Data with Airflow

## Overview

Sparkify is music company that has millions of users and has such deal with large amounts of data on daily basis. Sparkify aims to introduce more automation and monitoring to their data warehouse ETL pipelines. To assist with this automation process sparkify decided to use Apache Airflow.

## *What is Apache Airflow?*
Apache Airflow is a batch-oriented tool for building data pipelines. It is used to programmatically author, schedule, and monitor data pipelines commonly referred to as workflow orchestration. Airflow is an open-source platform used to manage the different tasks involved in processing data in a data pipeline. 

## *Benefits of Apache Airflow*
Airflow offers many benefits to organizations with extensive data pipelines. One of the benefits is that it is fully extendable, enabling you to customize operators with multiple databases, cloud services, and internal apps. Another benefit is that workflows are defined as code which makes them easy to maintain with better version control. 

## Goal
To create high grade dynamic data pipelines that are built from reusable tasks, can be monitored, and allow easy backfills. 

## Project Description

This project creates a high grade data pipeline that is dynamic and built from reusable tasks, can be monitored, and allow easy backfills. As data quality plays a big part when analyses are executed on top the data warehouse, thus the pipeline runs tests against Sparkify's datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Datasets
Here are the s3 links for datasets used in this project:

`Log data: s3://udacity-dend/log_data`
`Song data: s3://udacity-dend/song_data`

## Structure

Project has two directories named `dags` and `plugins`. A create tables script is in the `airflow` directory and readme file are at root level:

- `create_tables.sql`: SQL create table statements provided with template.

**`dags` directory contains:**

- `sparkify_etl_dag.py`: Defines main DAG, tasks and link the tasks in required order.

**`plugins/operators` directory contains:**

- `stage_redshift.py`: Defines `StageToRedshiftOperator` to copy JSON data from S3 to staging tables in the Redshift via `copy` command.
- `load_dimension.py`: Defines `LoadDimensionOperator` to load a dimension table from staging table(s).
- `load_fact.py`: Defines `LoadFactOperator` to load fact table from staging table(s).
- `data_quality.py`: Defines `DataQualityOperator` to run data quality checks on all tables passed as parameter.
- `sql_queries.py`: Contains SQL queries for the ETL pipeline (provided in template).

## STAR Schema and DAG

### STAR Schema
![](images/Schema.png)

### Steps
1. Extract and Load (EL) data from JSON files stored on Amazon S3 into staging tables on AWS Redshift. No transformations are made in this step.
2. Extract, transform and load the data from staging tables into fact tables and dimension tables in AWS Redshift.
3. Data Quality checks are performed on the dimensional tables to see if the transformations ran correctly.

### DAG with the sequence of steps
![](images/DAG.png)

## Conclusion
Project demonstrates ability to build a Data Pipeline using APache Airflow.
