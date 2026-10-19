import os
import signal
import subprocess
import pytest
from django.contrib.auth.models import User
from django.db.backends.postgresql.client import DatabaseClient

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass')

def test_runshell_db_success(user):
    db_client = DatabaseClient()
    db_client.executable_name = 'psql'  # Assuming psql is in the environment

    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'test_db',
        'user': user.username,
        'password': 'testpass'
    }

    try:
        db_client.runshell_db(conn_params)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Unexpected CalledProcessError: {e}")

def test_runshell_db_no_user():
    db_client = DatabaseClient()
    db_client.executable_name = 'psql'

    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'test_db',
        'password': 'testpass'
    }

    try:
        db_client.runshell_db(conn_params)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Unexpected CalledProcessError: {e}")

def test_runshell_db_no_password():
    db_client = DatabaseClient()
    db_client.executable_name = 'psql'

    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'test_db',
        'user': 'testuser'
    }

    try:
        db_client.runshell_db(conn_params)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Unexpected CalledProcessError: {e}")

def test_runshell_db_handle_sigint(user):
    db_client = DatabaseClient()
    db_client.executable_name = 'psql'
    
    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'test_db',
        'user': user.username,
        'password': 'testpass'
    }

    # Simulating SIGINT handling.
    original_sigint = signal.getsignal(signal.SIGINT)
    try:
        db_client.runshell_db(conn_params)
    finally:
        signal.signal(signal.SIGINT, original_sigint)