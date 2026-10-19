import signal
from django.db.backends.base.client import BaseDatabaseClient
import pytest

class DatabaseClient(BaseDatabaseClient):
    executable_name = 'psql'

    @classmethod
    def settings_to_cmd_args_env(cls, settings_dict, parameters):
        args = [cls.executable_name]
        options = settings_dict.get("OPTIONS", {})

        host = settings_dict.get("HOST")
        port = settings_dict.get("PORT")
        dbname = settings_dict.get("NAME")
        user = settings_dict.get("USER")
        passwd = settings_dict.get("PASSWORD")
        passfile = options.get("passfile")
        service = options.get("service")
        sslmode = options.get("sslmode")
        sslrootcert = options.get("sslrootcert")
        sslcert = options.get("sslcert")
        sslkey = options.get("sslkey")

        if not dbname and not service:
            dbname = "postgres"
        if user:
            args += ["-U", user]
        if host:
            args += ["-h", host]
        if port:
            args += ["-p", str(port)]
        if dbname:
            args += [dbname]
        args.extend(parameters)

        env = {}
        if passwd:
            env["PGPASSWORD"] = str(passwd)
        if service:
            env["PGSERVICE"] = str(service)
        if sslmode:
            env["PGSSLMODE"] = str(sslmode)
        if sslrootcert:
            env["PGSSLROOTCERT"] = str(sslrootcert)
        if sslcert:
            env["PGSSLCERT"] = str(sslcert)
        if sslkey:
            env["PGSSLKEY"] = str(sslkey)
        if passfile:
            env["PGPASSFILE"] = str(passfile)
        return args, (env or None)

def test_settings_to_cmd_args_env():
    settings_dict = {
        "HOST": "localhost",
        "PORT": 5432,
        "NAME": "test_db",
        "USER": "test_user",
        "PASSWORD": "test_pass",
        "OPTIONS": {
            "passfile": "/path/to/passfile",
            "service": "test_service",
            "sslmode": "require",
            "sslrootcert": "/path/to/rootcert",
            "sslcert": "/path/to/cert",
            "sslkey": "/path/to/key"
        }
    }
    parameters = ['--some-parameter']
    expected_args = [
        'psql', 
        '-U', 'test_user', 
        '-h', 'localhost', 
        '-p', '5432', 
        'test_db',
        '--some-parameter'
    ]
    expected_env = {
        "PGPASSWORD": "test_pass",
        "PGSERVICE": "test_service",
        "PGSSLMODE": "require",
        "PGSSLROOTCERT": "/path/to/rootcert",
        "PGSSLCERT": "/path/to/cert",
        "PGSSLKEY": "/path/to/key",
        "PGPASSFILE": "/path/to/passfile"
    }

    args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

    assert args == expected_args
    assert env == expected_env

def test_settings_to_cmd_args_env_default_db():
    settings_dict = {
        "HOST": None,
        "PORT": None,
        "NAME": None,
        "USER": None,
        "PASSWORD": None,
        "OPTIONS": {}
    }
    parameters = []
    expected_args = ['psql', 'postgres']
    expected_env = None

    args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

    assert args == expected_args
    assert env == expected_env