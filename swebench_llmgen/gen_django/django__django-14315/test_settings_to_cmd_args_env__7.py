import pytest
from django.db.backends.postgresql.client import DatabaseClient

class TestDatabaseClient:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.client = DatabaseClient()
        self.client.executable_name = 'psql'

    def test_settings_to_cmd_args_env_with_all_params(self):
        settings_dict = {
            'HOST': 'localhost',
            'PORT': 5432,
            'NAME': 'mydb',
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'OPTIONS': {
                'passfile': '/path/to/passfile',
                'service': 'myservice',
                'sslmode': 'require',
                'sslrootcert': '/path/to/root.crt',
                'sslcert': '/path/to/cert.crt',
                'sslkey': '/path/to/key.key',
            }
        }
        parameters = ['-c', 'statement_timeout=30000']
        expected_args = [
            'psql', '-U', 'myuser', '-h', 'localhost', '-p', '5432', 'mydb', '-c', 'statement_timeout=30000'
        ]
        expected_env = {
            'PGPASSWORD': 'mypassword',
            'PGSERVICE': 'myservice',
            'PGSSLMODE': 'require',
            'PGSSLROOTCERT': '/path/to/root.crt',
            'PGSSLCERT': '/path/to/cert.crt',
            'PGSSLKEY': '/path/to/key.key',
            'PGPASSFILE': '/path/to/passfile',
        }
        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)
        assert args == expected_args
        assert env == expected_env

    def test_settings_to_cmd_args_env_with_default_db(self):
        settings_dict = {
            'HOST': 'localhost',
            'PORT': 5432,
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'OPTIONS': {},
        }
        parameters = []
        expected_args = [
            'psql', '-U', 'myuser', '-h', 'localhost', '-p', '5432', 'postgres'
        ]
        expected_env = {
            'PGPASSWORD': 'mypassword',
        }
        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)
        assert args == expected_args
        assert env == expected_env

    def test_settings_to_cmd_args_env_without_user(self):
        settings_dict = {
            'HOST': 'localhost',
            'PORT': 5432,
            'NAME': 'mydb',
            'OPTIONS': {},
        }
        parameters = []
        expected_args = [
            'psql', '-h', 'localhost', '-p', '5432', 'mydb'
        ]
        expected_env = {}
        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)
        assert args == expected_args
        assert env == expected_env

    def test_settings_to_cmd_args_env_empty_settings(self):
        settings_dict = {}
        parameters = []
        expected_args = ['psql', 'postgres']
        expected_env = {}
        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)
        assert args == expected_args
        assert env == expected_env