import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Extracts the data from JSON files in S3 buckets and copies them to two staging tables.
    Queries are stored as 'copy_table_queries' in sql_queries.py
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Transforms and Loads data from the relevant staging tables to the dimensional model.
    Queries are stored as 'insert_table_queries' in sql_queries.py'
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Read through configuration file to access credentials and configuration to AWS. 
    Establish connection to Database.
    First extract and load data into staging tables. 
    Transofrm and laod data from staging to relevant dimensional model.  
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()