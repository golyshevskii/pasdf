import logging
from inspect import currentframe
from datetime import datetime

from creds import AIRFLOW_DAGS_PATH
from dag_patterns import DAG_PATTERNS
from dag_patterns_builder import DAGPatterns


logger = logging.getLogger(__name__)


class DAGBuilder(DAGPatterns):
    def __init__(self, dags_data: list = None):
        """
        Args:
            dags_data: list of DAGs data from Google Sheets
        """
        self.dags_data = dags_data

    def build(self, pattern_index: int = DAG_PATTERNS[0]):
        """Build the DAG Python code string using Google worksheet data

        Args:
            pattern_name: string pattern name from dag_patterns.py script
        """
        frame = currentframe().f_code.co_name
        logger.info(f"{frame} → Start building DAGs")

        date = datetime().now().date()

        for data in self.dags_data:
            db = data[0]
            schema = data[1]
            table = data[2]
            columns = data[3]
            schedule = (
                self._build_schedule_crone_string(data[4])
                if data[4] != "None"
                else None
            )

            try:
                kwargs_data = {
                    "db": db,
                    "schema": schema,
                    "table": table,
                    "columns": columns,
                    "schedule": schedule,
                }
                dag_code_string = self._build_pattern(pattern_index, **kwargs_data)

                dag_file_name = "dag_%s_%s_%s_incremental_update.py" % (
                    db,
                    schema,
                    table,
                )
                self._build_file(dag_file_name, dag_code_string)
            except Exception as ex:
                logger.error(
                    f"{frame} → An error occurred while building the DAG code, data:\n%s",
                    data,
                    exc_info=ex,
                )

        logger.info(f"{frame} → DAGs built successfully")

    def _build_file(self, dag_file_name: str, dag_code_string: str):
        """Create Python file from the DAG code string

        Args:
            dag_file_name: string file name
            dag_code_string: string DAG code
        """
        with open(f"{AIRFLOW_DAGS_PATH}dags/{dag_file_name}.py", "w") as py_file:
            py_file.write(dag_code_string)
