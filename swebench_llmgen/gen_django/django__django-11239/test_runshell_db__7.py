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
        self.client.executable_name = 'psql'  # Set the executable name for the test

    def test_runshell_db_with_user(self, monkeypatch):
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_password'
        }

        def mock_run(args, check, env):
            assert args == ['psql', '-U', 'test_user', '-h', 'localhost', '-p', '5432', 'test_db']
            assert env['PGPASSWORD'] == 'test_password'
            return

        monkeypatch.setattr(subprocess, 'run', mock_run)

        self.client.runshell_db(conn_params)

    def test_runshell_db_without_user(self, monkeypatch):
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'password': 'test_password'
        }

        def mock_run(args, check, env):
            assert args == ['psql', '-h', 'localhost', '-p', '5432', 'test_db']
            assert env['PGPASSWORD'] == 'test_password'
            return

        monkeypatch.setattr(subprocess, 'run', mock_run)

        self.client.runshell_db(conn_params)

    def test_runshell_db_with_no_password(self, monkeypatch):
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'user': 'test_user'
        }

        def mock_run(args, check, env):
            assert args == ['psql', '-U', 'test_user', '-h', 'localhost', '-p', '5432', 'test_db']
            assert 'PGPASSWORD' not in env
            return

        monkeypatch.setattr(subprocess, 'run', mock_run)

        self.client.runshell_db(conn_params)

    def test_runshell_db_with_only_database(self, monkeypatch):
        conn_params = {
            'database': 'test_db'
        }

        def mock_run(args, check, env):
            assert args == ['psql', 'test_db']
            assert 'PGPASSWORD' not in env
            return

        monkeypatch.setattr(subprocess, 'run', mock_run)

        self.client.runshell_db(conn_params)