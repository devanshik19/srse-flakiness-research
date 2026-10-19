import os
import signal
import subprocess
import pytest
from django.contrib.auth.models import User
from django.db.backends.postgresql.client import DatabaseClient

@pytest.mark.parametrize("conn_params, expected_args", [
    ({"host": "localhost", "port": 5432, "database": "test_db", "user": "test_user", "password": "test_pass"}, 
     ['psql', '-U', 'test_user', '-h', 'localhost', '-p', '5432', 'test_db']),
    ({"database": "test_db"}, 
     ['psql', 'test_db']),
    ({"user": "test_user", "database": "test_db"}, 
     ['psql', '-U', 'test_user', 'test_db']),
])
def test_runshell_db(monkeypatch, conn_params, expected_args):
    DatabaseClient.executable_name = 'psql'
    
    def mock_subprocess_run(args, check, env):
        assert args == expected_args
        assert check is True
        assert env.get('PGPASSWORD') == conn_params.get('password', '')
    
    monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)
    
    DatabaseClient.runshell_db(conn_params)
    
    # Check if the PGPASSWORD environment variable is set correctly
    assert os.environ.get('PGPASSWORD') == conn_params.get('password', '')
    
    # Check that original signal handler is restored
    original_sigint_handler = signal.getsignal(signal.SIGINT)
    assert original_sigint_handler != signal.SIG_IGN