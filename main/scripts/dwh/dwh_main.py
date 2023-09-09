import logging

import psycopg2


logger = logging.getLogger(__name__)


class PostgreSQL:
    def __init__(self, conn_string: str = None, **kwargs) -> None:
        """
        Args:
            conn_string: connection string
            **kwargs: dictionary of connection parameters


            example:
            kwargs = {
                "host": "host",
                "port": "port",
                "database": "database",
                "username": "username",
                "password": "password",
            }
        """
        self.conn_string = conn_string

        if not self.conn_string:
            self.conn_data = kwargs

    def select(self, query: str) -> list:
        """
        Selects data from a PostgreSQL database

        Args:
            query: SQL query string

        Returns:
            A list of tuples containing the selected data
        """
        logger.info("Start extracting data from PostgreSQL database")

        if self.conn_string:
            conn = psycopg2.connect(self.conn_string)
        else:
            conn = psycopg2.connect(**self.conn_data)

        with conn.cursor() as cur:
            try:
                cur.execute(query)
                data = cur.fetchall()

                logger.info(
                    "Data from PostgreSQL database extracted, rows: %s",
                    cur.rowcount,
                )
                return data
            except psycopg2.Error as ex:
                logger.error(
                    "An error occurred while extracting data from PostgreSQL database",
                    exc_info=ex,
                )
                return []
