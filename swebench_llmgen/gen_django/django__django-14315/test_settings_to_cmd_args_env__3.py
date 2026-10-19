import pytest
from django.db.backends.postgresql.client import DatabaseClient

class TestDatabaseClient:
    
    @pytest.fixture
    def setup_client(self):
        client = DatabaseClient()
        client.executable_name = 'psql'
        return client

    def test_settings_to_cmd_args_env_default_db(self, setup_client):
        settings_dict = {
            'OPTIONS': {},
            'HOST': None,
            'PORT': None,
            'NAME': None,
            'USER': None,
            'PASSWORD': None,
        }
        parameters = []
        args, env = setup_client.settings_to_cmd_args_env(settings_dict, parameters)
        
        assert args == ['psql', 'postgres']
        assert env == {}

    def test_settings_to_cmd_args_env_with_user_and_host(self, setup_client):
        settings_dict = {
            'OPTIONS': {},
            'HOST': 'localhost',
            'PORT': 5432,
            'NAME': 'test_db',
            'USER': 'test_user',
            'PASSWORD': 'test_pass',
        }
        parameters = ['--no-password']
        args, env = setup_client.settings_to_cmd_args_env(settings_dict, parameters)
        
        assert args == ['psql', '-U', 'test_user', '-h', 'localhost', '-p', '5432', 'test_db', '--no-password']
        assert env == {'PGPASSWORD': 'test_pass'}

    def test_settings_to_cmd_args_env_with_ssl_options(self, setup_client):
        settings_dict = {
            'OPTIONS': {
                'sslmode': 'require',
                'sslrootcert': '/path/to/root.crt',
                'sslcert': '/path/to/cert.crt',
                'sslkey': '/path/to/key.key',
                'passfile': '/path/to/passfile',
            },
            'HOST': 'localhost',
            'PORT': 5432,
            'NAME': 'test_db',
            'USER': 'test_user',
            'PASSWORD': 'test_pass',
        }
        parameters = []
        args, env = setup_client.settings_to_cmd_args_env(settings_dict, parameters)
        
        assert args == ['psql', '-U', 'test_user', '-h', 'localhost', '-p', '5432', 'test_db']
        assert env == {
            'PGPASSWORD': 'test_pass',
            'PGSSLMODE': 'require',
            'PGSSLROOTCERT': '/path/to/root.crt',
            'PGSSLCERT': '/path/to/cert.crt',
            'PGSSLKEY': '/path/to/key.key',
            'PGPASSFILE': '/path/to/passfile',
        }

    def test_settings_to_cmd_args_env_with_service(self, setup_client):
        settings_dict = {
            'OPTIONS': {},
            'HOST': None,
            'PORT': None,
            'NAME': None,
            'USER': 'test_user',
            'PASSWORD': 'test_pass',
            'SERVICE': 'my_service',
        }
        parameters = []
        args, env = setup_client.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == ['psql', '-U', 'test_user', 'postgres']
        assert env == {'PGPASSWORD': 'test_pass', 'PGSERVICE': 'my_service'}