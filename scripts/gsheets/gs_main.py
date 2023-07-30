from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from logger import logger

log = logger("gs_main.py")


class GoogleSheets:
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self, service_account_creds: dict) -> None:
        self.creds = service_account_creds

    def _make_credentials(self):
        """Method that creates the credentials from the service account data"""
        try:
            return Credentials.from_service_account_info(self.creds, scopes=self.SCOPE)
        except Exception as ex:
            log.error(ex)
            raise ex

    def get_spreadsheet_data(self, spreadsheet_id: str, sheet_name: str):
        """Method that returns the data from a spreadsheet"""
        try:
            log.info("Getting data from spreadsheet")
            creds: Credentials = self._make_credentials()
            service = build("sheets", "v4", credentials=creds)

            values: dict = (
                service.spreadsheets()
                .values()
                .get(
                    spreadsheetId=spreadsheet_id,
                    range=f"{sheet_name}!A:ZZ",
                    majorDimension="ROWS",
                )
                .execute()
            )
        except (HttpError, Exception) as ex:
            log.error(ex)
            raise ex

        log.info("Data from spreadsheet extracted")
        return values.get("values", [])
