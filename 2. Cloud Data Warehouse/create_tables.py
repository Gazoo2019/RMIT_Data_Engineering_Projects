import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    drops the two staging tables and tables that are part of the dimensional model.
    Queries are stored as 'drop_table_queries' in sql_queries.py'
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates the staging tables as well as fact and dimensional tables.
    Queries are stored as 'create_table_queries' in sql_queries.py'
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Read through configuration file to access credentials and configuration to AWS. 
    Establish connection to Database.
    First drop tables and their contents. 
    Create all the relvant tables as per the table creating queries. 
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()