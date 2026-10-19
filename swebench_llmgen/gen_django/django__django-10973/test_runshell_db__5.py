import os
import pytest
import signal
import subprocess
from django.contrib.auth.models import User
from django.db.backends.postgresql.client import DatabaseClient

@pytest.fixture
def db_client():
    client = DatabaseClient()
    client.executable_name = 'psql'  # Assuming psql is accessible
    return client

def test_runshell_db_with_password(db_client):
    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'testdb',
        'user': 'testuser',
        'password': 'testpassword',
    }

    # Create a temporary user for testing if needed
    User.objects.create_user(username='testuser', password='testpassword')

    try:
        db_client.runshell_db(conn_params)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"psql command failed with exit code {e.returncode}")

def test_runshell_db_without_password(db_client):
    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'testdb',
        'user': 'testuser',
        'password': '',
    }

    # Create a temporary user for testing if needed
    User.objects.create_user(username='testuser', password='testpassword')

    try:
        db_client.runshell_db(conn_params)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"psql command failed with exit code {e.returncode}")

def test_runshell_db_with_invalid_params(db_client):
    conn_params = {
        'host': 'invalid_host',
        'port': 12345,
        'database': 'invalid_db',
        'user': 'invalid_user',
        'password': 'invalid_password',
    }

    with pytest.raises(subprocess.CalledProcessError):
        db_client.runshell_db(conn_params)

def test_runshell_db_sigint_handler(db_client):
    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'testdb',
        'user': 'testuser',
        'password': 'testpassword',
    }

    # Create a temporary user for testing if needed
    User.objects.create_user(username='testuser', password='testpassword')

    original_sigint = signal.getsignal(signal.SIGINT)
    try:
        # This test can't effectively assert SIGINT handling in subprocess directly
        # But we confirm that no exceptions are raised up to the subprocess call
        db_client.runshell_db(conn_params)
    finally:
        signal.signal(signal.SIGINT, original_sigint)