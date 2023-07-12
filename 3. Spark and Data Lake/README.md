# Data Lake with Apache Spark

## Purpose 

Build an ETL pipeline that extracts song and log data from an S3 bucket, processes the data using Spark and finally loads the data back into s3 as a set of dimensional tables in spark parquet files. 

**Motivation**
To helps analysts quickly obtain insights on users listening preferences.

## Schema Design

Using a STAR schema which will contain the following: 

**1 fact table** 
- *songplays* 

**4 dimensional tables**
- *users*
- *songs*
- *artists*
- *time* 

The above schema is suitable for OLAP(Online Analytical Processing) operations. 

## Files

**etl.py**
This script once executed retrieves the song and log data in the s3 bucket, transforms the data into fact and dimensional tables then loads the table data back into s3 as parquet files.

**dl.cfg**
Should contain your AWS keys.

## Getting Started
The following instructions will help you run teh project on your local computer. 

### Prerequisites
   - Python 2.7 or greater.
   - AWS Account.

   - Set your AWS access and secret key in the config file. 
        ```
        [AWS]
        AWS_ACCESS_KEY_ID = <your aws key>
        AWS_SECRET_ACCESS_KEY = <your aws secret>
        ```

### Installation
   - Make a new directory and clone/copy project files into it.
   - Download and install Apache Spark here https://spark.apache.org/downloads.html. Also ensure you have Java jdk8 installed locally.
   - Create a virtualenv that will be your development environment, i.e:
       ```
       $ virtualenv data-lakes-project
       $ source data-lakes-project/bin/activate
       ```
   - Install the following packages in your virtual environment:

            - pyspark

- Alternatively you can install the requirements in the `requirements.txt` that's in this project by running the command:
    ```
    $ pip install -r requirements.txt
     ```
            
### Terminal commands
- Execute the ETL pipeline script by running:
    ```
    $ python etl.py
    ```

## Built With
- Python and pySpark