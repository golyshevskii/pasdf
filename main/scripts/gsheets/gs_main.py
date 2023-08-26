import logging

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


class GoogleSheets:
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self, service_account_creds: dict) -> None:
        """
        Args:
            service_account_creds: dictionary service account credentials data
        """
        self.creds = service_account_creds

    def _make_credentials(self) -> Credentials:
        """
        Creates the credentials from the service account data

        Returns: service account Credentials instance
        """
        return Credentials.from_service_account_info(self.creds, scopes=self.SCOPE)

    def get_worksheet_data(self, spreadsheet_id: str, sheet_name: str) -> list:
        """
        Extracts the data from a worksheet

        Args:
            spreadsheet_id: string spreadsheet id
            sheet_name: string sheet name

        Returns: list of spreedsheet data
        """
        logger.info("Start extracting data from %s worksheet", sheet_name)

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

        data = values.get("values", [])

        logger.info("Data from %s worksheet extracted, rows: %s", sheet_name, len(data))
        return data

    def update_worksheet_data(
        self, spreadsheet_id: str, sheet_name: str, data: list, range: str = "A2:Z"
    ) -> None:
        """
        Updates data in a worksheet

        Args:
            spreadsheet_id: string spreadsheet id
            sheet_name: string sheet name
            data: list of data to update
            range: string of columns range to update
        """
        logger.info("Start updating data in %s worksheet", sheet_name)

        creds: Credentials = self._make_credentials()
        service = build("sheets", "v4", credentials=creds)

        body = {"values": data}

        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!{range}",
            valueInputOption="RAW",
            body=body,
        ).execute()

        logger.info("%s worksheet data updated", sheet_name)
