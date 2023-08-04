import psycopg2

from logger import logger

log = logger(__name__)


class PostgreSQL:
    def __init__(self, **kwargs) -> None:
        """
        **kwargs: dictionary of connection parameters
            example:
            kwargs = {
                "conn_string": f"postgresql://{username}:{password}@{host}:{port}/{dbname}",
                "host": "host",
                "port": "port",
                "database": "database",
                "username": "username",
                "password": "password",
            }
        """
        self.conn_string = kwargs.get("conn_string")

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
        if self.conn_string:
            conn = psycopg2.connect(self.conn_string)
        else:
            conn = psycopg2.connect(**self.conn_data)

        with conn.cursor() as cur:
            try:
                cur.execute(query)
                data = cur.fetchall()

                log.info("Data extracted successfully")
                return data
            except psycopg2.Error as ex:
                log.error("An error occurred while extracting data", exc_info=ex)
                return []
