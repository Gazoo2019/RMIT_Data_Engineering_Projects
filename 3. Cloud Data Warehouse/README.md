# Sparkify User Action Analysis 
*using S3 and Redshift*

### Introduction

This project focuses on transferring Sparify's artis and song database processes on to the cloud. An ETL pipline  is established between **AWS S3** and **AWS Redshift**.  

**AWS S3:** Focuses on data stroage. Two public datasets are stored in two public **S3 buckets** which contain *(1)* info about songs and artists and *(2) User Actions.*

**AWS Redshift:** This is a service where data will be ingested and transformed. `COPY` command we will access to the JSON files inside the buckets and copy their content on our *staging tables*.

### Database Schema
Consists two staging tables which *copy* the JSON file inside the  **S3 buckets**. Plan to use a STAR schema to optimise for queries on song playlists. 

#### Staging Table 
- **staging_songs** - info about songs and artists
- **staging_events** - actions done by users (which song are listening, etc.. )

#### Fact Table 
- **songplays** - records in event data associated with song plays i.e. records with page `NextSong`

#### Dimension Tables
- **users** - users in the app
- **songs** - songs in music database
- **artists** - artists in music database
- **time** - timestamps of records in **songplays** broken down into specific units


### Data Warehouse Configurations and Setup
* Create a new `IAM user` in your AWS account
* Give it AdministratorAccess and Attach policies
* Use access key and secret key to create clients for `EC2`, `S3`, `IAM`, and `Redshift`.
* Create an `IAM Role` that makes `Redshift` able to access `S3 bucket` (ReadOnly)
* Create a `RedShift Cluster` and get the `DWH_ENDPOIN(Host address)` and `DWH_ROLE_ARN` and fill the config file.

### ETL Pipeline
- Created tables to store the data from `S3 buckets`.
- Loading the data from `S3 buckets` to staging tables in the `Redshift Cluster`.
- Inserted data into fact and dimension tables from the staging tables.

### Project Structure

- `create_tables.py` - This script will drop old tables (if exist) ad re-create new tables.
- `etl.py` - This script executes the queries that extract `JSON` data from the `S3 bucket` and ingest them to `Redshift`.
- `sql_queries.py` - This file contains variables with SQL statement in String formats, partitioned by `CREATE`, `DROP`, `COPY` and `INSERT` statement.
- `dhw.cfg` - Configuration file used that contains info about `Redshift`, `IAM` and `S3`

### How to Run

1. Create tables by running `create_tables.py`.

2. Execute ETL process by running `etl.py`.
