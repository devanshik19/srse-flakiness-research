import signal
from django.db.backends.base.client import BaseDatabaseClient
import pytest

class DatabaseClient(BaseDatabaseClient):
    executable_name = 'psql'

    @classmethod
    def settings_to_cmd_args_env(cls, settings_dict, parameters):
        args = [cls.executable_name]
        options = settings_dict.get('OPTIONS', {})

        host = settings_dict.get('HOST')
        port = settings_dict.get('PORT')
        dbname = settings_dict.get('NAME')
        user = settings_dict.get('USER')
        passwd = settings_dict.get('PASSWORD')
        passfile = options.get('passfile')
        service = options.get('service')
        sslmode = options.get('sslmode')
        sslrootcert = options.get('sslrootcert')
        sslcert = options.get('sslcert')
        sslkey = options.get('sslkey')

        if not dbname and not service:
            dbname = 'postgres'
        if user:
            args += ['-U', user]
        if host:
            args += ['-h', host]
        if port:
            args += ['-p', str(port)]
        if dbname:
            args += [dbname]
        args.extend(parameters)

        env = {}
        if passwd:
            env['PGPASSWORD'] = str(passwd)
        if service:
            env['PGSERVICE'] = str(service)
        if sslmode:
            env['PGSSLMODE'] = str(sslmode)
        if sslrootcert:
            env['PGSSLROOTCERT'] = str(sslrootcert)
        if sslcert:
            env['PGSSLCERT'] = str(sslcert)
        if sslkey:
            env['PGSSLKEY'] = str(sslkey)
        if passfile:
            env['PGPASSFILE'] = str(passfile)
        return args, env

@pytest.mark.parametrize("settings_dict, parameters, expected_args, expected_env", [
    (
        {'HOST': 'localhost', 'PORT': 5432, 'NAME': 'test_db', 'USER': 'user', 'PASSWORD': 'pass'},
        [],
        ['psql', '-U', 'user', '-h', 'localhost', '-p', '5432', 'test_db'],
        {'PGPASSWORD': 'pass'}
    ),
    (
        {'OPTIONS': {'service': 'myservice'}, 'USER': 'user'},
        [],
        ['psql', '-U', 'user'],
        {'PGSERVICE': 'myservice'}
    ),
    (
        {'NAME': 'mydb'},
        ['--options'],
        ['psql', '-U', 'user', 'mydb', '--options'],
        {}
    ),
    (
        {'OPTIONS': {'sslmode': 'require'}, 'PASSWORD': 'mypassword'},
        [],
        ['psql', '-U', 'user', 'postgres'],
        {'PGPASSWORD': 'mypassword', 'PGSSLMODE': 'require'}
    ),
    (
        {'OPTIONS': {'passfile': '/path/to/passfile'}},
        [],
        ['psql', 'postgres'],
        {'PGPASSFILE': '/path/to/passfile'}
    ),
])
def test_settings_to_cmd_args_env(settings_dict, parameters, expected_args, expected_env):
    client = DatabaseClient()
    # Set default user for the test context
    settings_dict['USER'] = 'user'
    args, env = client.settings_to_cmd_args_env(settings_dict, parameters)
    assert args == expected_args
    assert env == expected_env