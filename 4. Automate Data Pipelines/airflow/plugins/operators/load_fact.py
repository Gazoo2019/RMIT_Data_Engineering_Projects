from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    """
    DAG operator used to populate fact tables.
    :param string  redshift_conn_id: reference to a specific redshift database
    :param string  table_name: redshift table to load
    :param string  insert_sql: statement used to extract songplays data
    """

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 table_name,
                 insert_sql,
                 *args,
                 **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table_name = table_name
        self.insert_sql = insert_sql

    def execute(self, context):
        self.log.info('LoadFactOperator begin execute')
        # connect to Redshift
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info(f"...connected with {self.redshift_conn_id}")

        # build insert statement
        sql_stmt = f"INSERT INTO {self.table_name} {self.insert_sql}"
        self.log.info(f"insert sql: {sql_stmt}")

        redshift_hook.run(sql_stmt)
        self.log.info(
            f"StageToRedshiftOperator insert complete - {self.table_name}")