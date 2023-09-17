PATTERN_0 = """from datetime import datetime, timedelta

from scripts.airflow.airflow_table_update import update_table_incremental

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


dag_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "task_concurrency": 1,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="%s",
    description="%s",
    start_date=datetime(%s),
    default_args=dag_args,
    schedule_interval=%s,
    tags=%s,
    catchup=False,
) as dag:
    # TASKS
    dag_start = EmptyOperator(task_id="dag_start")

    task_kwargs = {
        "db": "%s",
        "schema": "%s",
        "table": "%s",
        "columns": "%s",
    }

    task_%s_update = PythonOperator(
        task_id="task_%s_update",
        python_callable=update_table_incremental,
        ops_kwargs=task_kwargs,
        provide_context=True,
    )

    dag_end = EmptyOperator(task_id="dag_end")

    # TASK CHAIN
    dag_start >> task_%s_update >> dag_end

"""

PATTERNS = {
    0: PATTERN_0,
}
