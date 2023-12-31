from unittest.mock import patch

from scripts.etl.etl_gs_dwh_update import update_dwh_worksheet_data


@patch("scripts.etl.etl_gs_dwh_update.open")
@patch("scripts.etl.etl_gs_dwh_update.PostgreSQL")
@patch("scripts.etl.etl_gs_dwh_update.GoogleSheets")
def test_update_dwh_worksheet_data(
    mock_open, mock_postgresql, mock_googlesheets, caplog
):
    # Call the function to be tested
    update_dwh_worksheet_data()

    # Assertions
    mock_open.assert_called_once()

    mock_postgresql.assert_called_once()
    mock_postgresql.return_value.select.assert_called_once()

    mock_googlesheets.assert_called_once()
