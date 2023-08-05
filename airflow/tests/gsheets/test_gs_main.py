import sys

sys.path.append("/Users/python_poseur/pasdf_develop/pasdf/airflow/")

from unittest.mock import MagicMock, patch

import pytest
from creds import GS_SPREADSHEET_ID
from scripts.gsheets.gs_main import GoogleSheets


class TestGoogleSheets:
    DAG_SHEET_NAME = "DAG"
    DWH_SHEET_NAME = "DWH"

    GET_DATA = [
        [
            "postgres",
            "public",
            "h_user",
            "id;business_key;created_dt",
            "every day at 00:00",
        ],
    ]
    UPDATE_DATA = [["postgres", "raw"]]

    @pytest.fixture
    def mock_credentials(self, monkeypatch):
        mock_creds = MagicMock()
        monkeypatch.setattr(
            "scripts.gsheets.gs_main.Credentials.from_service_account_info", mock_creds
        )
        return mock_creds

    @pytest.fixture
    def mock_service(self, monkeypatch):
        mock_service = MagicMock()
        monkeypatch.setattr("scripts.gsheets.gs_main.build", mock_service)
        return mock_service

    def test_get_spreadsheet_data(self, mock_credentials, mock_service):
        mock_service_instance = mock_service.return_value
        mock_spreadsheets = mock_service_instance.spreadsheets.return_value
        mock_values_method = (
            mock_spreadsheets.values.return_value.get.return_value.execute
        )
        mock_values_method.return_value = {"values": self.GET_DATA}

        gs = GoogleSheets(mock_credentials)
        data = gs.get_worksheet_data(GS_SPREADSHEET_ID, self.DAG_SHEET_NAME)

        assert data == self.GET_DATA

    def test_update_spreadsheet_data(self, mock_credentials, mock_service):
        mock_service_instance = mock_service.return_value
        mock_spreadsheets = mock_service_instance.spreadsheets.return_value
        mock_values_method = (
            mock_spreadsheets.values.return_value.update.return_value.execute
        )

        gs = GoogleSheets(mock_credentials)

        with patch.object(gs, "_make_credentials", return_value=mock_credentials):
            gs.update_worksheet_data(
                GS_SPREADSHEET_ID, self.DWH_SHEET_NAME, self.UPDATE_DATA, "A2:B"
            )

        # Assert that the necessary methods were called with the expected arguments
        mock_service.assert_called_once_with(
            "sheets", "v4", credentials=mock_credentials
        )
        mock_spreadsheets.values.return_value.update.assert_called_once_with(
            spreadsheetId=GS_SPREADSHEET_ID,
            range=f"{self.DWH_SHEET_NAME}!A2:B",
            valueInputOption="RAW",
            body={"values": self.UPDATE_DATA},
        )
        mock_values_method.assert_called_once()
