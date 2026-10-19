import pytest
from django.db.backends.postgresql.client import DatabaseClient


@pytest.fixture
def db_client():
    client = DatabaseClient()
    client.executable_name = 'psql'
    return client


def test_settings_to_cmd_args_env_with_dbname(db_client):
    settings_dict = {
        "NAME": "test_db",
        "USER": "test_user",
        "PASSWORD": "test_pass",
        "HOST": "localhost",
        "PORT": 5432,
        "OPTIONS": {}
    }
    parameters = ['--some-parameter']
    expected_args = ['psql', '-U', 'test_user', '-h', 'localhost', '-p', '5432', 'test_db', '--some-parameter']
    expected_env = {"PGPASSWORD": "test_pass"}
    
    args, env = db_client.settings_to_cmd_args_env(settings_dict, parameters)
    
    assert args == expected_args
    assert env == expected_env


def test_settings_to_cmd_args_env_with_service(db_client):
    settings_dict = {
        "SERVICE": "test_service",
        "OPTIONS": {}
    }
    parameters = []
    expected_args = ['psql', 'postgres']
    expected_env = {"PGSERVICE": "test_service"}
    
    args, env = db_client.settings_to_cmd_args_env(settings_dict, parameters)
    
    assert args == expected_args
    assert env == expected_env


def test_settings_to_cmd_args_env_without_dbname_and_service(db_client):
    settings_dict = {
        "OPTIONS": {}
    }
    parameters = []
    expected_args = ['psql', 'postgres']
    expected_env = {}
    
    args, env = db_client.settings_to_cmd_args_env(settings_dict, parameters)
    
    assert args == expected_args
    assert env is None


def test_settings_to_cmd_args_env_with_ssl_options(db_client):
    settings_dict = {
        "NAME": "test_db",
        "USER": "test_user",
        "PASSWORD": "test_pass",
        "OPTIONS": {
            "sslmode": "require",
            "sslrootcert": "/path/to/root.crt",
            "sslcert": "/path/to/cert.crt",
            "sslkey": "/path/to/key.key",
            "passfile": "/path/to/passfile"
        }
    }
    parameters = []
    expected_args = ['psql', '-U', 'test_user', 'test_db']
    expected_env = {
        "PGPASSWORD": "test_pass",
        "PGSSLMODE": "require",
        "PGSSLROOTCERT": "/path/to/root.crt",
        "PGSSLCERT": "/path/to/cert.crt",
        "PGSSLKEY": "/path/to/key.key",
        "PGPASSFILE": "/path/to/passfile"
    }
    
    args, env = db_client.settings_to_cmd_args_env(settings_dict, parameters)
    
    assert args == expected_args
    assert env == expected_env