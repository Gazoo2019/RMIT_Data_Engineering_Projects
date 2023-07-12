# ETL Pipeline for Immigration and Temperature Data

### Project Summary

The goal of this project is to create an ETL pipeline using I94 immigration data and city temperature data to form a database that is optimized for queries on immigration events. This database can be used to answer questions relating immigration behavior to destination temperature e.g., do people tend to immigrate to warmer places?
The project follows the follow steps:

* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up

---

### Project Scope and Data Description

#### Scope
This project will integrate I94 immigration data, world temperature data and US demographic data to setup a data warehouse with fact and dimension tables.

* Data Sets 
    1. [I94 Immigration Data](https://travel.trade.gov/research/reports/i94/historical/2016.html)
    2. [World Temperature Data](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data)
    3. [U.S. City Demographic Data](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/)


#### Describe and Gather Data 

| Data Set | Format | Description |
| ---      | ---    | ---         |
|[I94 Immigration Data](https://travel.trade.gov/research/reports/i94/historical/2016.html)| SAS | Data contains international visitor arrival statistics by world regions and select countries (including top 20), type of visa, mode of transportation, age groups, states visited (first intended address only), and the top ports of entry (for select countries).|
|[World Temperature Data](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data)| CSV | This dataset is from Kaggle and contains monthly average temperature data at different country in the world wide.|
|[U.S. City Demographic Data](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/)| CSV | This dataset contains information about the demographics of all US cities and census-designated places with a population greater or equal to 65,000.|


---

### Key Summary of Project

#### Tools and Technologies
- **`Spark:`** *Spark was chosen since it can easily handle multiple file formats (including SAS) containing large amounts of data.* 
- **`Spark SQL:`** *Spark SQL was chosen to process the large input files into dataframes and manipulated via standard SQL join operations to form additional tables.*


#### Data Update Frequency
Tables created from immigration and temperature data set should be updated monthly since the raw data set is built up monthly.


#### Future Design Considerations
1. The data was increased by 100x.
	
	If Spark with standalone server mode can not process 100x data set, we could consider to put data in [AWS EMR](https://aws.amazon.com/tw/emr/?nc2=h_ql_prod_an_emr&whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc) which is a distributed data cluster for processing large data sets on cloud

2. The data populates a dashboard that must be updated on a daily basis by 7am every day.

	[Apache Airflow](https://airflow.apache.org) could be used for building up a ETL data pipeline to regularly update the date and populate a report. Apache Airflow also integrate with Python and AWS very well. More applications can be combined together to deliever more powerful task automation.

3. The database needed to be accessed by 100+ people.

	[AWS Redshift](https://aws.amazon.com/tw/redshift/?nc2=h_ql_prod_db_rs&whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc) can handle up to 500 connections. If this SSOT database will be accessed by 100+ people, we can move this database to Redshift with confidence to handle this request. Cost/Benefit analysis will be needed if we are going be implement this cloud solution.

---

### Future Improvements
There are several incompletions within these data sets. We will need to collect more data to get a more complete SSOT database.

1. Immigration data set is based at 2016 but temperature data set only get to 2013 which is not enough for us to see the temperature change at 2016.
	
2. Missing state and city in label description file. This makes it hard to join immigration tables and demography tables.