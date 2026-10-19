import os
import signal
import subprocess
import pytest
from django.contrib.auth.models import User
from django.db.backends.postgresql.client import DatabaseClient

class TestDatabaseClient:

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.client = DatabaseClient()
        self.client.executable_name = 'psql'  # Assuming this is set to 'psql' for testing

    def test_runshell_db_with_password(self, monkeypatch):
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_password',
        }

        monkeypatch.setattr(subprocess, 'check_call', lambda args: None)
        
        with pytest.raises(SystemExit):
            self.client.runshell_db(conn_params)

    def test_runshell_db_without_password(self, monkeypatch):
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'user': 'test_user',
            'password': '',
        }

        monkeypatch.setattr(subprocess, 'check_call', lambda args: None)
        
        with pytest.raises(SystemExit):
            self.client.runshell_db(conn_params)

    def test_runshell_db_with_unicode_error(self, monkeypatch):
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_password',
        }

        monkeypatch.setattr(subprocess, 'check_call', lambda args: None)
        monkeypatch.setattr(os, 'environ', {})

        assert os.environ.get('PGPASSFILE') is None
        
        self.client.runshell_db(conn_params)
        
        assert os.environ.get('PGPASSFILE') is None

    def test_runshell_db_resets_sigint_handler(self, monkeypatch):
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_password',
        }

        original_handler = signal.getsignal(signal.SIGINT)

        monkeypatch.setattr(subprocess, 'check_call', lambda args: None)

        self.client.runshell_db(conn_params)

        assert signal.getsignal(signal.SIGINT) == original_handler