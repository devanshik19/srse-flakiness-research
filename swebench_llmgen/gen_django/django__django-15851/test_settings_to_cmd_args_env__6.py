import pytest
from django.db.backends.postgresql.client import DatabaseClient

@pytest.fixture
def database_client():
    client = DatabaseClient()
    client.executable_name = "psql"  # Example executable name
    return client

def test_settings_to_cmd_args_env(database_client):
    settings_dict = {
        "HOST": "localhost",
        "PORT": 5432,
        "NAME": "test_db",
        "USER": "test_user",
        "PASSWORD": "test_pass",
        "OPTIONS": {
            "passfile": "/path/to/passfile",
            "service": None,
            "sslmode": "require",
            "sslrootcert": "/path/to/sslrootcert",
            "sslcert": "/path/to/sslcert",
            "sslkey": "/path/to/sslkey",
        }
    }
    parameters = ["--some-parameter"]

    args, env = database_client.settings_to_cmd_args_env(settings_dict, parameters)

    assert args == [
        "psql",
        "-U", "test_user",
        "-h", "localhost",
        "-p", "5432",
        "test_db",
        "--some-parameter"
    ]

    assert env == {
        "PGPASSWORD": "test_pass",
        "PGPASSFILE": "/path/to/passfile",
        "PGSSLMODE": "require",
        "PGSSLROOTCERT": "/path/to/sslrootcert",
        "PGSSLCERT": "/path/to/sslcert",
        "PGSSLKEY": "/path/to/sslkey",
    }

def test_settings_to_cmd_args_env_no_db_service(database_client):
    settings_dict = {
        "HOST": None,
        "PORT": None,
        "NAME": None,
        "USER": None,
        "PASSWORD": None,
        "OPTIONS": {}
    }
    parameters = []

    args, env = database_client.settings_to_cmd_args_env(settings_dict, parameters)

    assert args == [
        "psql",
        "postgres"  # Default database should be used
    ]
    assert env is None

def test_settings_to_cmd_args_env_with_service(database_client):
    settings_dict = {
        "HOST": "localhost",
        "PORT": 5432,
        "NAME": None,
        "USER": "test_user",
        "PASSWORD": "test_pass",
        "OPTIONS": {
            "service": "my_service",
        }
    }
    parameters = []

    args, env = database_client.settings_to_cmd_args_env(settings_dict, parameters)

    assert args == [
        "psql",
        "-U", "test_user",
        "-h", "localhost",
        "-p", "5432",
        "postgres"  # Default database since NAME is None
    ]
    assert env == {
        "PGSERVICE": "my_service"
    }