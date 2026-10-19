import os
import signal
import subprocess
import pytest
from django.contrib.auth.models import User
from django.db.backends.postgresql.client import DatabaseClient

class TestDatabaseClient:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = DatabaseClient()
        self.client.executable_name = 'psql'  # Set the executable name to test
        
    def test_runshell_db_with_password(self, monkeypatch):
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_password'
        }

        def mock_check_call(args):
            assert args == [
                'psql', '-U', 'test_user', '-h', 'localhost',
                '-p', '5432', 'test_db'
            ]
            return 0

        monkeypatch.setattr(subprocess, 'check_call', mock_check_call)

        with monkeypatch.context() as m:
            m.setattr(signal, 'signal', lambda sig, handler: None)
            self.client.runshell_db(conn_params)

        assert 'PGPASSFILE' in os.environ  # Ensure PGPASSFILE was set
        assert os.path.exists(os.environ['PGPASSFILE'])  # Check the temp file exists

        os.remove(os.environ['PGPASSFILE'])  # Cleanup after test

    def test_runshell_db_without_password(self, monkeypatch):
        conn_params = {
            'host': '',
            'port': '',
            'database': 'test_db',
            'user': '',
            'password': ''
        }

        def mock_check_call(args):
            assert args == ['psql', 'test_db']
            return 0

        monkeypatch.setattr(subprocess, 'check_call', mock_check_call)

        with monkeypatch.context() as m:
            m.setattr(signal, 'signal', lambda sig, handler: None)
            self.client.runshell_db(conn_params)

        assert 'PGPASSFILE' not in os.environ  # Ensure PGPASSFILE was not set