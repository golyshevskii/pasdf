import logging
import sys
from datetime import datetime

sys.path.append("/Users/python_poseur/pasdf_develop/pasdf/")

from creds import PATH
from dag_patterns import DAG_PATTERN_INCREMENTAL_TABLE_UPDATE

logger = logging.getLogger(__name__)


class DAGBuilder:
    def __init__(self, dags_data: list = None):
        """
        Args:
            dags_data: list of DAGs data from Google Sheets
        """
        self.dags_data = dags_data

    def build(self, pattern_name: str = DAG_PATTERN_INCREMENTAL_TABLE_UPDATE):
        """Build the DAG Python code string using Google worksheet data

        Args:
            pattern_name: string pattern name from dag_patterns.py script
        """
        logger.info("Start building DAGs")

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
                dag_code_string = pattern_name % (
                    db,
                    schema,
                    table,
                    db,
                    schema,
                    table,
                    date.year,
                    date.month,
                    date.day,
                    schedule,
                    db,
                    schema,
                    table,
                    columns,
                    table,
                    table,
                    table,
                )

                dag_file_name = "dag_%s_%s_%s_incremental_update.py" % (
                    db,
                    schema,
                    table,
                )
                self._build_file(dag_file_name, dag_code_string)
            except Exception as ex:
                logger.error(
                    "An error occurred while building the DAG code, data:\n%s",
                    data,
                    exc_info=ex,
                )

        logger.info("DAGs built successfully")

    def _build_schedule_crone_string(self, schedule: str = "0 0 * * *"):
        pass

    def _build_code_string(self):
        pass

    def _build_file(self, dag_file_name: str, dag_code_string: str):
        """Create Python file from the DAG code string

        Args:
            dag_file_name: string file name
            dag_code_string: string DAG code
        """
        with open(f"{PATH}dags/{dag_file_name}.py", "w") as py_file:
            py_file.write(dag_code_string)
