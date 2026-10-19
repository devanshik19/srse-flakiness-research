import os
import signal
import subprocess
import pytest
from django.contrib.auth.models import User
from django.db.backends.postgresql.client import DatabaseClient

@pytest.fixture
def database_client():
    client = DatabaseClient()
    client.executable_name = 'psql'  # Assume psql is available in the environment.
    return client

def test_runshell_db_with_user(database_client, monkeypatch):
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

    monkeypatch.setattr(subprocess, 'run', mock_run)

    database_client.runshell_db(conn_params)

def test_runshell_db_without_user(database_client, monkeypatch):
    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'test_db',
        'password': 'test_password'
    }

    def mock_run(args, check, env):
        assert args == ['psql', '-h', 'localhost', '-p', '5432', 'test_db']
        assert env['PGPASSWORD'] == 'test_password'

    monkeypatch.setattr(subprocess, 'run', mock_run)

    database_client.runshell_db(conn_params)

def test_runshell_db_no_password(database_client, monkeypatch):
    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'test_db',
        'user': 'test_user'
    }

    def mock_run(args, check, env):
        assert args == ['psql', '-U', 'test_user', '-h', 'localhost', '-p', '5432', 'test_db']
        assert 'PGPASSWORD' not in env  # Confirm that PGPASSWORD is not set

    monkeypatch.setattr(subprocess, 'run', mock_run)

    database_client.runshell_db(conn_params)

def test_runshell_db_no_params(database_client, monkeypatch):
    conn_params = {
        'database': 'test_db'
    }

    def mock_run(args, check, env):
        assert args == ['psql', 'test_db']
        assert 'PGPASSWORD' not in env  # Confirm that PGPASSWORD is not set

    monkeypatch.setattr(subprocess, 'run', mock_run)

    database_client.runshell_db(conn_params)