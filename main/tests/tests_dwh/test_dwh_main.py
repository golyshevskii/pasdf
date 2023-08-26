import unittest
from unittest.mock import MagicMock, patch

from psycopg2 import Error
from scripts.dwh.dwh_main import PostgreSQL


class TestPostgreSQL(unittest.TestCase):
    DATA = [
        (1, "hub_user"),
        (2, "hub_store"),
    ]

    def setUp(self):
        conn_data = {
            "host": "dummy_host",
            "port": "dummy_port",
            "database": "dummy_db",
            "username": "dummy_user",
            "password": "dummy_password",
        }
        self.pg_conn_data = PostgreSQL(**conn_data)
        self.pg_conn_string = PostgreSQL(conn_string="dummy_conn_string")

    def test_select_with_conn_string(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = self.DATA

        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect = MagicMock(return_value=mock_connection)

        with patch("psycopg2.connect", mock_connect):
            result = self.pg_conn_string.select("SELECT * FROM hubs")

        self.assertEqual(result, self.DATA)

        mock_connect.assert_called_once_with("dummy_conn_string")
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM hubs")
        mock_cursor.fetchall.assert_called_once()

    def test_select_with_conn_data(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = self.DATA

        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect = MagicMock(return_value=mock_connection)

        with patch("psycopg2.connect", mock_connect):
            result = self.pg_conn_data.select("SELECT * FROM hubs")

        self.assertEqual(result, self.DATA)

        mock_connect.assert_called_once_with(
            host="dummy_host",
            port="dummy_port",
            database="dummy_db",
            username="dummy_user",
            password="dummy_password",
        )
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM hubs")
        mock_cursor.fetchall.assert_called_once()

    def test_select_error_handling(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = Error("Mocked error")

        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect = MagicMock(return_value=mock_connection)

        with patch("psycopg2.connect", mock_connect):
            result = self.pg_conn_string.select("SELECT * FROM hubs")

        self.assertEqual(result, [])

        mock_connect.assert_called_once_with("dummy_conn_string")
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM hubs")
        mock_cursor.fetchall.assert_called_once()
