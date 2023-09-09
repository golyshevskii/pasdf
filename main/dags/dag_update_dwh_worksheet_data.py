from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from scripts.etl.etl_gs_dwh_update import update_dwh_worksheet_data


dag_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "task_concurrency": 1,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="dag_update_dwh_worksheet_data",
    description="Update data in a Google DWH worksheet",
    start_date=datetime(2023, 8, 11),
    default_args=dag_args,
    schedule_interval=None,
    tags=["gs", "worksheet"],
    catchup=False,
) as dag:
    """Updates data in a Google DWH worksheet"""

    dag_start = EmptyOperator(task_id="dag_start")

    task_update_dwh_worksheet_data = PythonOperator(
        task_id="task_update_dwh_worksheet_data",
        python_callable=update_dwh_worksheet_data,
        provide_context=True,
    )

    dag_end = EmptyOperator(task_id="dag_end")

    # task chain
    dag_start >> task_update_dwh_worksheet_data >> dag_end
