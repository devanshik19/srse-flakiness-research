import pytest
from django.db.backends.postgresql.client import DatabaseClient

def test_settings_to_cmd_args_env_with_all_options():
    settings_dict = {
        "OPTIONS": {
            "passfile": "path/to/passfile",
            "service": "my_service",
            "sslmode": "require",
            "sslrootcert": "path/to/sslrootcert",
            "sslcert": "path/to/sslcert",
            "sslkey": "path/to/sslkey"
        },
        "HOST": "localhost",
        "PORT": 5432,
        "NAME": "test_db",
        "USER": "test_user",
        "PASSWORD": "test_password"
    }
    parameters = ["--some-parameter"]
    expected_args = [
        DatabaseClient.executable_name,
        "-U", "test_user",
        "-h", "localhost",
        "-p", "5432",
        "test_db",
        "--some-parameter"
    ]
    expected_env = {
        "PGPASSWORD": "test_password",
        "PGSERVICE": "my_service",
        "PGSSLMODE": "require",
        "PGSSLROOTCERT": "path/to/sslrootcert",
        "PGSSLCERT": "path/to/sslcert",
        "PGSSLKEY": "path/to/sslkey",
        "PGPASSFILE": "path/to/passfile"
    }
    
    args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)
    
    assert args == expected_args
    assert env == expected_env

def test_settings_to_cmd_args_env_with_default_db():
    settings_dict = {
        "OPTIONS": {},
        "HOST": None,
        "PORT": None,
        "NAME": None,
        "USER": None,
        "PASSWORD": None
    }
    parameters = []
    expected_args = [DatabaseClient.executable_name, "postgres"]
    expected_env = None

    args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)
    
    assert args == expected_args
    assert env == expected_env

def test_settings_to_cmd_args_env_with_only_user_and_host():
    settings_dict = {
        "OPTIONS": {},
        "HOST": "127.0.0.1",
        "PORT": None,
        "NAME": "test_db",
        "USER": "admin",
        "PASSWORD": "admin_password"
    }
    parameters = []
    expected_args = [
        DatabaseClient.executable_name,
        "-U", "admin",
        "-h", "127.0.0.1",
        "test_db"
    ]
    expected_env = {
        "PGPASSWORD": "admin_password"
    }

    args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

    assert args == expected_args
    assert env == expected_env