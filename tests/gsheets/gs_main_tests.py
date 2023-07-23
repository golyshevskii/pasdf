import sys

sys.path.append("/Users/python_poseur/pasdf_develop/pasdf/")

from creds import GOOGLE_SHEETS_CREDENTIALS, GS_SPREADSHEET_ID
from logger import logger
from scripts.gsheets.gs_main import GoogleSheets

log = logger("gs_main_tests.py")


def test_get_data_from_google_sheets():
    """Function that tests the get_data_from_google_sheets function"""
    SHEET_NAME = "DAG"
    gs = GoogleSheets(GOOGLE_SHEETS_CREDENTIALS)

    data = gs.get_spreadsheet_data(GS_SPREADSHEET_ID, SHEET_NAME)
    assert data[0] == ['db', 'schema', 'table', 'columns', 'schedule']
    assert len(data) == 2

    log.info("test_get_data_from_google_sheets: PASSED")


if __name__ == "__main__":
    log.info("TESTS: START")

    test_get_data_from_google_sheets()

    log.info("TESTS: END")
