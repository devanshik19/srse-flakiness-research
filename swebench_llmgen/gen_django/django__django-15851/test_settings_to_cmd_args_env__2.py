import pytest
from django.contrib.auth.models import User
from django.db.backends.postgresql.client import DatabaseClient

class TestDatabaseClient:
    def test_settings_to_cmd_args_env_with_all_options(self):
        settings_dict = {
            'OPTIONS': {
                'passfile': 'test.pass',
                'service': 'test_service',
                'sslmode': 'require',
                'sslrootcert': 'root.crt',
                'sslcert': 'cert.pem',
                'sslkey': 'key.pem',
            },
            'HOST': 'localhost',
            'PORT': 5432,
            'NAME': 'test_db',
            'USER': 'test_user',
            'PASSWORD': 'test_password',
        }
        parameters = ['--param1=value1', '--param2=value2']

        expected_args = [
            DatabaseClient.executable_name, 
            '-U', 'test_user', 
            '-h', 'localhost', 
            '-p', '5432', 
            'test_db', 
            '--param1=value1', 
            '--param2=value2'
        ]
        expected_env = {
            'PGPASSWORD': 'test_password',
            'PGSERVICE': 'test_service',
            'PGSSLMODE': 'require',
            'PGSSLROOTCERT': 'root.crt',
            'PGSSLCERT': 'cert.pem',
            'PGSSLKEY': 'key.pem',
            'PGPASSFILE': 'test.pass',
        }

        args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == expected_args
        assert env == expected_env

    def test_settings_to_cmd_args_env_with_default_db(self):
        settings_dict = {
            'OPTIONS': {},
            'HOST': None,
            'PORT': None,
            'NAME': None,
            'USER': None,
            'PASSWORD': None,
        }
        parameters = []

        expected_args = [DatabaseClient.executable_name, 'postgres']
        expected_env = None

        args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == expected_args
        assert env == expected_env

    def test_settings_to_cmd_args_env_with_partial_info(self):
        settings_dict = {
            'OPTIONS': {},
            'HOST': 'localhost',
            'PORT': 5432,
            'NAME': 'test_db',
            'USER': 'test_user',
            'PASSWORD': 'test_password'
        }
        parameters = []

        expected_args = [
            DatabaseClient.executable_name, 
            '-U', 'test_user', 
            '-h', 'localhost', 
            '-p', '5432', 
            'test_db'
        ]
        expected_env = {
            'PGPASSWORD': 'test_password'
        }

        args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == expected_args
        assert env == expected_env

    def test_settings_to_cmd_args_env_with_service(self):
        settings_dict = {
            'OPTIONS': {},
            'HOST': None,
            'PORT': None,
            'NAME': None,
            'USER': None,
            'PASSWORD': None,
            'service': 'test_service'
        }
        parameters = []

        expected_args = [DatabaseClient.executable_name, 'postgres']
        expected_env = {
            'PGSERVICE': 'test_service'
        }

        args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == expected_args
        assert env == expected_env