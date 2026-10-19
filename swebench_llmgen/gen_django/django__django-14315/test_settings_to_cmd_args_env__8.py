import pytest
from django.db.backends.postgresql.client import DatabaseClient

class TestDatabaseClient:

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.client = DatabaseClient()
        self.client.executable_name = 'psql'  # Setup executable_name for testing

    def test_settings_to_cmd_args_env_with_dbname(self):
        settings_dict = {
            'NAME': 'test_db',
            'USER': 'test_user',
            'PASSWORD': 'test_pass',
            'HOST': 'localhost',
            'PORT': '5432',
            'OPTIONS': {}
        }
        parameters = ['--no-password']
        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == ['psql', '-U', 'test_user', '-h', 'localhost', '-p', '5432', 'test_db', '--no-password']
        assert env == {'PGPASSWORD': 'test_pass'}

    def test_settings_to_cmd_args_env_without_dbname(self):
        settings_dict = {
            'USER': 'test_user',
            'PASSWORD': 'test_pass',
            'OPTIONS': {}
        }
        parameters = []
        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == ['psql', '-U', 'test_user', 'postgres']
        assert env == {'PGPASSWORD': 'test_pass'}

    def test_settings_to_cmd_args_env_with_ssl_options(self):
        settings_dict = {
            'NAME': 'test_db',
            'USER': 'test_user',
            'PASSWORD': 'test_pass',
            'HOST': 'localhost',
            'OPTIONS': {
                'sslmode': 'require',
                'sslrootcert': '/path/to/root.crt',
                'sslcert': '/path/to/cert.crt',
                'sslkey': '/path/to/key.key',
                'passfile': '/path/to/passfile',
            }
        }
        parameters = []
        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == [
            'psql', '-U', 'test_user', '-h', 'localhost', 'test_db'
        ]
        assert env == {
            'PGPASSWORD': 'test_pass',
            'PGSSLMODE': 'require',
            'PGSSLROOTCERT': '/path/to/root.crt',
            'PGSSLCERT': '/path/to/cert.crt',
            'PGSSLKEY': '/path/to/key.key',
            'PGPASSFILE': '/path/to/passfile',
        }

    def test_settings_to_cmd_args_env_with_service(self):
        settings_dict = {
            'SERVICE': 'test_service',
            'OPTIONS': {}
        }
        parameters = []
        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == ['psql', 'postgres']
        assert env == {'PGSERVICE': 'test_service'}