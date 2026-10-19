import os
import signal
import subprocess
import pytest
from django.contrib.auth.models import User
from django.db.backends.postgresql.client import DatabaseClient

@pytest.fixture
def db_client():
    client = DatabaseClient()
    client.executable_name = 'psql'  # Assuming psql is installed and accessible
    return client

def test_runshell_db_with_password(db_client):
    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'testdb',
        'user': 'testuser',
        'password': 'testpass',
    }

    # Create a temporary .pgpass file
    with pytest.raises(subprocess.CalledProcessError):
        db_client.runshell_db(conn_params)

    assert 'PGPASSFILE' in os.environ

def test_runshell_db_without_password(db_client):
    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'testdb',
        'user': 'testuser',
        'password': '',
    }

    with pytest.raises(subprocess.CalledProcessError):
        db_client.runshell_db(conn_params)

    # Ensure PGPASSFILE is no longer set
    assert 'PGPASSFILE' not in os.environ

def test_runshell_db_with_only_db_name(db_client):
    conn_params = {
        'database': 'testdb',
    }

    with pytest.raises(subprocess.CalledProcessError):
        db_client.runshell_db(conn_params)

    # Ensure PGPASSFILE is not set
    assert 'PGPASSFILE' not in os.environ

def test_runshell_db_with_invalid_user(db_client):
    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'testdb',
        'user': 'invaliduser',
        'password': 'dummy',
    }

    with pytest.raises(subprocess.CalledProcessError):
        db_client.runshell_db(conn_params)

    assert 'PGPASSFILE' not in os.environ