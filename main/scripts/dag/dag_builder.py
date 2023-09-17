import logging
from inspect import currentframe

import dag_patterns as PATTERNS


logger = logging.getLogger(__name__)


class DAGBuilder:
    METHODS = {
        0: "_build_0"
    }
    
    def _create_schedule(self, schedule: str = "0 0 * * *") -> str:
        return schedule

    def _build_0(self, **kwargs) -> str:
        """Build pattern with index 0
        
        Args:
            **kwargs: dictionary of the DAG data
            db: database name string
            schema: schema name string
            table: table name string
            columns: columns string
            schedule: crone schedule string
        
        Returns: string Python DAG code
        """
        frame = currentframe().f_code.co_name
        logger.info(f"{frame} → Start building 0 pattern")
    
    def _build(self, **kwargs) -> str:
        """Choose the DAG pattern to build
        
        Returns: string Python DAG code
        """
        pattern = kwargs["pattern"]
        method = getattr(DAGBuilder, self.METHODS[pattern])
        
        code = method(**kwargs)
        return code
        