import logging
import sys

sys.path.append("/Users/python_poseur/pasdf_develop/pasdf/")

from creds import GS_CREDS, GS_SPREADSHEET_ID, PATH, PSQL_CONN_STRING
from scripts.dwh.dwh_main import PostgreSQL
from scripts.gsheets.gs_main import GoogleSheets

logger = logging.getLogger(__name__)


def update_dwh_worksheet_data(**kwargs) -> None:
    """Updates data in a DWH Google spreadsheet"""
    logger.info("Start updating data in DWH worksheet")

    with open(
        f"{PATH}sql/psql/psql_tables_data.sql",
        "r",
        encoding="utf-8",
    ) as sql_file:
        PSQL_QUERY = sql_file.read()

    pg = PostgreSQL(conn_string=PSQL_CONN_STRING)
    data = pg.select(query=PSQL_QUERY)

    gs = GoogleSheets(GS_CREDS)
    gs.update_worksheet_data(GS_SPREADSHEET_ID, "DWH", data)

    logger.info("DWH worksheet data updated")
