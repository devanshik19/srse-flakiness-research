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
        self.client.executable_name = 'psql'

    def test_runshell_db_with_required_params(self, monkeypatch):
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'user': 'test_user',
            'password': 'secret'
        }

        def mock_run(*args, **kwargs):
            assert args[0] == ['psql', '-U', 'test_user', '-h', 'localhost', '-p', '5432', 'test_db']
            assert kwargs['env']['PGPASSWORD'] == 'secret'
            return subprocess.CompletedProcess(args, 0)

        monkeypatch.setattr(subprocess, 'run', mock_run)
        self.client.runshell_db(conn_params)

    def test_runshell_db_without_user(self, monkeypatch):
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'password': 'secret'
        }

        def mock_run(*args, **kwargs):
            assert args[0] == ['psql', '-h', 'localhost', '-p', '5432', 'test_db']
            assert 'PGPASSWORD' not in kwargs['env']
            return subprocess.CompletedProcess(args, 0)

        monkeypatch.setattr(subprocess, 'run', mock_run)
        self.client.runshell_db(conn_params)

    def test_runshell_db_without_password(self, monkeypatch):
        conn_params = {
            'host': '',
            'port': '',
            'database': 'test_db',
            'user': 'test_user'
        }

        def mock_run(*args, **kwargs):
            assert args[0] == ['psql', '-U', 'test_user', 'test_db']
            assert 'PGPASSWORD' not in kwargs['env']
            return subprocess.CompletedProcess(args, 0)

        monkeypatch.setattr(subprocess, 'run', mock_run)
        self.client.runshell_db(conn_params)