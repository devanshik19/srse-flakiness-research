import pytest
from django.db.backends.postgresql.client import DatabaseClient

@pytest.fixture
def db_client():
    # Return an instance of the DatabaseClient with the executable_name set
    client = DatabaseClient()
    client.executable_name = 'psql'
    return client

def test_settings_to_cmd_args_env_no_dbname_or_service(db_client):
    settings_dict = {
        'HOST': None,
        'PORT': None,
        'NAME': None,
        'USER': None,
        'PASSWORD': None,
        'OPTIONS': {}
    }
    parameters = []
    args, env = db_client.settings_to_cmd_args_env(settings_dict, parameters)
    assert args == ['psql', 'postgres']
    assert env == {}

def test_settings_to_cmd_args_env_with_user(db_client):
    settings_dict = {
        'HOST': 'localhost',
        'PORT': 5432,
        'NAME': 'testdb',
        'USER': 'testuser',
        'PASSWORD': 'secret',
        'OPTIONS': {}
    }
    parameters = []
    args, env = db_client.settings_to_cmd_args_env(settings_dict, parameters)
    assert args == ['psql', '-U', 'testuser', '-h', 'localhost', '-p', '5432', 'testdb']
    assert env == {'PGPASSWORD': 'secret'}

def test_settings_to_cmd_args_env_with_options(db_client):
    settings_dict = {
        'HOST': 'localhost',
        'PORT': 5432,
        'NAME': 'testdb',
        'USER': 'testuser',
        'PASSWORD': 'secret',
        'OPTIONS': {
            'passfile': '/path/to/passfile',
            'service': 'myservice',
            'sslmode': 'require',
            'sslrootcert': '/path/to/sslrootcert',
            'sslcert': '/path/to/sslcert',
            'sslkey': '/path/to/sslkey'
        }
    }
    parameters = []
    args, env = db_client.settings_to_cmd_args_env(settings_dict, parameters)
    assert args == ['psql', '-U', 'testuser', '-h', 'localhost', '-p', '5432', 'testdb']
    assert env == {
        'PGPASSWORD': 'secret',
        'PGSERVICE': 'myservice',
        'PGSSLMODE': 'require',
        'PGSSLROOTCERT': '/path/to/sslrootcert',
        'PGSSLCERT': '/path/to/sslcert',
        'PGSSLKEY': '/path/to/sslkey',
        'PGPASSFILE': '/path/to/passfile'
    }

def test_settings_to_cmd_args_env_with_no_password(db_client):
    settings_dict = {
        'HOST': 'localhost',
        'PORT': 5432,
        'NAME': 'testdb',
        'USER': 'testuser',
        'PASSWORD': None,
        'OPTIONS': {}
    }
    parameters = []
    args, env = db_client.settings_to_cmd_args_env(settings_dict, parameters)
    assert args == ['psql', '-U', 'testuser', '-h', 'localhost', '-p', '5432', 'testdb']
    assert env == {}