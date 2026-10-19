import pytest
from django.db.backends.postgresql.client import DatabaseClient

class TestDatabaseClient:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        # Setting up the class variable as a placeholder for testing.
        DatabaseClient.executable_name = 'postgres'

    def test_settings_to_cmd_args_env_default_db(self):
        settings_dict = {
            'HOST': None,
            'PORT': None,
            'NAME': None,
            'USER': None,
            'PASSWORD': None,
            'OPTIONS': {}
        }
        parameters = []

        args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == ['postgres', 'postgres']
        assert env == {}

    def test_settings_to_cmd_args_env_with_user(self):
        settings_dict = {
            'HOST': 'localhost',
            'PORT': 5432,
            'NAME': 'mydb',
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'OPTIONS': {}
        }
        parameters = []

        args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == ['postgres', '-U', 'myuser', '-h', 'localhost', '-p', '5432', 'mydb']
        assert env == {'PGPASSWORD': 'mypassword'}

    def test_settings_to_cmd_args_env_with_ssl_options(self):
        settings_dict = {
            'HOST': 'localhost',
            'PORT': 5432,
            'NAME': 'mydb',
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'OPTIONS': {
                'sslmode': 'require',
                'sslrootcert': '/path/to/root.crt',
                'sslcert': '/path/to/client.crt',
                'sslkey': '/path/to/client.key',
                'passfile': '/path/to/passfile',
            }
        }
        parameters = []

        args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == [
            'postgres', 
            '-U', 'myuser', 
            '-h', 'localhost', 
            '-p', '5432', 
            'mydb'
        ]
        assert env == {
            'PGPASSWORD': 'mypassword',
            'PGSSLMODE': 'require',
            'PGSSLROOTCERT': '/path/to/root.crt',
            'PGSSLCERT': '/path/to/client.crt',
            'PGSSLKEY': '/path/to/client.key',
            'PGPASSFILE': '/path/to/passfile'
        }

    def test_settings_to_cmd_args_env_with_service(self):
        settings_dict = {
            'HOST': None,
            'PORT': None,
            'NAME': None,
            'USER': None,
            'PASSWORD': None,
            'OPTIONS': {
                'service': 'my_service'
            }
        }
        parameters = []

        args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == ['postgres', 'postgres']
        assert env == {'PGSERVICE': 'my_service'}