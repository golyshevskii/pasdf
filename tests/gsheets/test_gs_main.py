import sys

sys.path.append("/Users/python_poseur/pasdf_develop/pasdf/")

from unittest.mock import MagicMock

import pytest

from creds import GOOGLE_SHEETS_CREDENTIALS, GS_SPREADSHEET_ID
from scripts.gsheets.gs_main import GoogleSheets


class TestGoogleSheets:
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
        mock_values = {
            "values": [["id", "key"], ["1", "1234-qwer"], ["2", "qwer-1234"]]
        }

        mock_service_instance = mock_service.return_value
        mock_spreadsheets = mock_service_instance.spreadsheets.return_value
        mock_values_method = (
            mock_spreadsheets.values.return_value.get.return_value.execute
        )
        mock_values_method.return_value = mock_values

        sheet_name = "DAG"

        gs = GoogleSheets(GOOGLE_SHEETS_CREDENTIALS)
        data = gs.get_spreadsheet_data(GS_SPREADSHEET_ID, sheet_name)

        assert data == mock_values["values"]
