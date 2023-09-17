import logging
from inspect import currentframe

from creds import AIRFLOW_DAGS_PATH
from dag_builder import DAGBuilder


logger = logging.getLogger(__name__)


class PyDAG(DAGBuilder):
    def __init__(self, data: dict = None) -> None:
        """
        Args:
            dags_data: list of DAGs data from Google Sheets
        """
        self.data = data
    
    def _create_file(self, file_name: str, code_str: str):
        """Create Python file from the DAG code string

        Args:
            file_name: string file name
            code_str: string DAG code
        """
        with open(f"{AIRFLOW_DAGS_PATH}dags/{file_name}.py", "w") as file:
            file.write(code_str)

    def build(self):
        """Build the DAG Python code string using Google worksheet data"""
        frame = currentframe().f_code.co_name
        logger.info(f"{frame} → Start building DAG")

        if not self.data:
            logger.warning(f"{frame} → No DAG data provided")
            return

        code_str = self._build(**self.data)
        file_name = f"dag_{self.data['dag_id']}"

        self._create_file(file_name, code_str)
        logger.info(f"{frame} → DAG built successfully")
