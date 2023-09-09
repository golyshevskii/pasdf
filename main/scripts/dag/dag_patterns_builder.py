import logging
from inspect import currentframe

import dag_patterns_builder as dpb


logger = logging.getLogger(__name__)


class DAGPatterns:
    def _build_pattern(self, pattern_index: int, **kwargs) -> str:
        """Choose the DAG pattern to build
        
        Args:
            pattern_name: string pattern name from dag_patterns.py script
        """
        if pattern_index == 0:
            return self._build_incremental_table_update(**kwargs)
    
    def _build_schedule_crone_string(self, schedule: str = "0 0 * * *") -> str:
        return schedule

    def _build_incremental_table_update(self, **kwargs) -> str:
        """Build the incremental table update DAG Python code string
        
        Args:
            **kwargs: dictionary of the DAG data
            db: database name string
            schema: schema name string
            table: table name string
            columns: columns string
            schedule: crone schedule string
        """
        frame = currentframe().f_code.co_name
        logger.info(f"{frame} → Start building the DAG")

        pattern = dpb.DAG_PATTERN_INCREMENTAL_TABLE_UPDATE


        DAG_STR = ""
        return DAG_STR
        