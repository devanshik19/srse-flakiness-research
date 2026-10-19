import pytest
from django.db.backends.postgresql.client import DatabaseClient

@pytest.fixture
def database_client():
    client = DatabaseClient()
    client.executable_name = 'psql'
    return client

def test_settings_to_cmd_args_env_with_dbname(database_client):
    settings = {
        'HOST': 'localhost',
        'PORT': 5432,
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_pass',
        'OPTIONS': {}
    }
    parameters = []
    args, env = database_client.settings_to_cmd_args_env(settings, parameters)
    assert args == ['psql', '-U', 'test_user', '-h', 'localhost', '-p', '5432', 'test_db']
    assert env == {'PGPASSWORD': 'test_pass'}

def test_settings_to_cmd_args_env_with_service(database_client):
    settings = {
        'NAME': None,
        'OPTIONS': {'service': 'test_service'}
    }
    parameters = []
    args, env = database_client.settings_to_cmd_args_env(settings, parameters)
    assert args == ['psql', 'postgres']
    assert env == {'PGSERVICE': 'test_service'}

def test_settings_to_cmd_args_env_empty(database_client):
    settings = {
        'OPTIONS': {}
    }
    parameters = []
    args, env = database_client.settings_to_cmd_args_env(settings, parameters)
    assert args == ['psql', 'postgres']
    assert env == {}

def test_settings_to_cmd_args_env_with_ssl_options(database_client):
    settings = {
        'HOST': 'localhost',
        'PORT': 5432,
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_pass',
        'OPTIONS': {
            'sslmode': 'require',
            'sslrootcert': '/path/to/root.crt',
            'sslcert': '/path/to/cert.crt',
            'sslkey': '/path/to/key.key',
            'passfile': '/path/to/passfile'
        }
    }
    parameters = []
    args, env = database_client.settings_to_cmd_args_env(settings, parameters)
    assert args == ['psql', '-U', 'test_user', '-h', 'localhost', '-p', '5432', 'test_db']
    assert env == {
        'PGPASSWORD': 'test_pass',
        'PGSSLMODE': 'require',
        'PGSSLROOTCERT': '/path/to/root.crt',
        'PGSSLCERT': '/path/to/cert.crt',
        'PGSSLKEY': '/path/to/key.key',
        'PGPASSFILE': '/path/to/passfile'
    }