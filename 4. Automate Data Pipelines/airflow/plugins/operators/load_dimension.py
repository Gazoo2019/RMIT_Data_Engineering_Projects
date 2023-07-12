from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
    """
    DAG operator used to populate dimension tables  in a STAR schema.
    :param string  redshift_conn_id: reference to a specific redshift database
    :param string  table_name: redshift dimension table to load
    :param string  insert_sql: statement used to extract songplays data
    :param string  truncate_table: 'Y' truncates table before load; 'N' appends
    """

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 table_name,
                 insert_sql,
                 truncate_table,
                 *args,
                 **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table_name = table_name
        self.insert_sql = insert_sql
        self.truncate_table = truncate_table

    def execute(self, context):
        self.log.info('LoadDimensionOperator begin execute')
        # connect to Redshift
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info(f"...connected with {self.redshift_conn_id}")

        if self.truncate_table == 'Y':
            self.log.info(
                f"...truncating table {self.table_name} before adding records")
            redshift_hook.run(f"TRUNCATE TABLE {self.table_name}")

        # build insert statement
        insert_sql_stmt = f"INSERT INTO {self.table_name} {self.insert_sql}"
        self.log.info(f"...insert sql: {insert_sql_stmt}")

        redshift_hook.run(insert_sql_stmt)
        self.log.info(
            f"LoadDimensionOperator insert complete - {self.table_name}")