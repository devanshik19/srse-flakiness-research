import os
import signal
import subprocess
import pytest
from django.contrib.auth.models import User
from django.db.backends.postgresql.client import DatabaseClient

@pytest.fixture
def database_client():
    client = DatabaseClient()
    client.executable_name = 'psql'  # Assuming 'psql' is the command used.
    return client

def test_runshell_db_with_password(database_client, monkeypatch):
    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'test_db',
        'user': 'test_user',
        'password': 'test_pass'
    }
    
    # Mock subprocess.check_call to avoid actually running psql.
    monkeypatch.setattr(subprocess, 'check_call', lambda *args, **kwargs: None)

    with monkeypatch.context() as m:
        m.setattr("builtins.print", lambda *args, **kwargs: None)  # Mock print to suppress output
        # Test successful execution
        database_client.runshell_db(conn_params)

    # Test environment variable is set
    assert 'PGPASSFILE' in os.environ
    assert os.path.isfile(os.environ['PGPASSFILE'])
    
    # Cleanup the environment variable
    del os.environ['PGPASSFILE']

def test_runshell_db_without_password(database_client, monkeypatch):
    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'test_db',
        'user': 'test_user',
        'password': ''  # No password
    }

    # Mock subprocess.check_call to avoid actually running psql.
    monkeypatch.setattr(subprocess, 'check_call', lambda *args, **kwargs: None)

    with monkeypatch.context() as m:
        m.setattr("builtins.print", lambda *args, **kwargs: None)  # Mock print to suppress output
        # Test execution without password
        database_client.runshell_db(conn_params)

    # Ensure that PGPASSFILE is not set
    assert 'PGPASSFILE' not in os.environ

def test_runshell_db_without_user(database_client, monkeypatch):
    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'test_db',
        'user': '',  # No user
        'password': 'test_pass'
    }

    # Mock subprocess.check_call to avoid actually running psql.
    monkeypatch.setattr(subprocess, 'check_call', lambda *args, **kwargs: None)

    with monkeypatch.context() as m:
        m.setattr("builtins.print", lambda *args, **kwargs: None)  # Mock print to suppress output
        # Test execution without user
        database_client.runshell_db(conn_params)

    # Ensure that PGPASSFILE is set
    assert 'PGPASSFILE' in os.environ
    assert os.path.isfile(os.environ['PGPASSFILE'])
    
    # Cleanup the environment variable
    del os.environ['PGPASSFILE']