from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

# Insert your Key in here. 
# AWS_KEY = os.environ.get('')
# AWS_SECRET = os.environ.get('')

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2022, 1, 2),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}

dag = DAG('songplay_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *',
          max_active_runs=1
         )

start_task = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id="Stage_events",
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    destination_table="public.staging_events",
    json_paths="s3://udacity-dend/log_json_path.json",
    s3_bucket="udacity-dend",
    s3_key="log_data",
    #role_arn='',
    aws_region="us-west-2"
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id="Stage_songs",
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    destination_table="public.staging_songs",
    json_paths="auto",
    s3_bucket="udacity-dend",
    s3_key="song_data",
    #role_arn='',
    aws_region="us-west-2"
)

load_songplays_table = LoadFactOperator(
    task_id="Load_songplays_fact_table",
    dag=dag,
    redshift_conn_id="redshift",
    target_db="dev",
    destination_table="public.songplays",
    sql=SqlQueries.songplay_table_insert
)

load_user_dimension_table = LoadDimensionOperator(
    task_id="Load_user_dim_table",
    dag=dag,
    redshift_conn_id="redshift",
    target_db="dev",
    destination_table="public.users",
    sql=SqlQueries.user_table_insert,
    truncate=True
)

load_song_dimension_table = LoadDimensionOperator(
    task_id="Load_song_dim_table",
    dag=dag,
    redshift_conn_id="redshift",
    target_db="dev",
    destination_table="public.songs",
    sql=SqlQueries.song_table_insert,
    truncate=True
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id="Load_artist_dim_table",
    dag=dag,
    redshift_conn_id="redshift",
    target_db="dev",
    destination_table="public.artists",
    sql=SqlQueries.artist_table_insert,
    truncate=True
)

load_time_dimension_table = LoadDimensionOperator(
    task_id="Load_time_dim_table",
    dag=dag,
    redshift_conn_id="redshift",
    target_db="dev",
    destination_table="public.time",
    sql=SqlQueries.time_table_insert,
    truncate=True
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    tables=["public.songplays", "public.artists", "public.time", "public.songs", "public.users"]
)

end_task = DummyOperator(task_id='Stop_execution',  dag=dag)

start_task  >> [ stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table >> [
    load_user_dimension_table,
    load_song_dimension_table,
    load_artist_dimension_table,
    load_time_dimension_table
] >> run_quality_checks >> end_task