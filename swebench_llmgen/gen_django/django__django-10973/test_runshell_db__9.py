import os
import signal
import subprocess
import pytest
from django.core.files.temp import NamedTemporaryFile
from django.db.backends.postgresql.client import DatabaseClient
from django.contrib.auth.models import User

class TestDatabaseClient:

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.client = DatabaseClient()
        self.client.executable_name = 'psql'  # Assuming psql is installed

    def test_runshell_db_with_password(self, monkeypatch):
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_password'
        }
        
        def mock_check_call(args, **kwargs):
            assert args == [
                'psql',
                '-U', 'test_user',
                '-h', 'localhost',
                '-p', '5432',
                'test_db'
            ]
            return 0
        
        monkeypatch.setattr(subprocess, 'check_call', mock_check_call)
        monkeypatch.setattr(NamedTemporaryFile, 'close', lambda self: None)
        
        with monkeypatch.context() as m:
            m.setattr('os.environ', {})
            self.client.runshell_db(conn_params)
            assert os.environ['PGPASSFILE'] == ''

    def test_runshell_db_without_password(self, monkeypatch):
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'user': '',
            'password': ''
        }
        
        def mock_check_call(args, **kwargs):
            assert args == [
                'psql',
                '-h', 'localhost',
                '-p', '5432',
                'test_db'
            ]
            return 0
        
        monkeypatch.setattr(subprocess, 'check_call', mock_check_call)
        
        with monkeypatch.context() as m:
            m.setattr('os.environ', {})
            self.client.runshell_db(conn_params)

    def test_runshell_db_with_unicode_error(self, monkeypatch):
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'user': 'test_user',
            'password': 'password_with_unicode_©'
        }
        
        def mock_check_call(args, **kwargs):
            return 0
        
        monkeypatch.setattr(subprocess, 'check_call', mock_check_call)
        monkeypatch.setattr(NamedTemporaryFile, 'close', lambda self: None)

        with pytest.raises(UnicodeEncodeError):
            self.client.runshell_db(conn_params)