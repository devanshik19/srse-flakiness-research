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

def test_settings_to_cmd_args_env():
    settings_dict = {
        'OPTIONS': {
            'passfile': '/path/to/passfile',
            'service': 'myservice',
            'sslmode': 'require',
            'sslrootcert': '/path/to/root.crt',
            'sslcert': '/path/to/cert.crt',
            'sslkey': '/path/to/key.key',
        },
        'HOST': 'localhost',
        'PORT': 5432,
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_pass'
    }
    parameters = ['--some-param', 'value']

    expected_args = [
        'psql',
        '-U', 'test_user',
        '-h', 'localhost',
        '-p', '5432',
        'test_db',
        '--some-param', 'value'
    ]
    
    expected_env = {
        'PGPASSWORD': 'test_pass',
        'PGSERVICE': 'myservice',
        'PGSSLMODE': 'require',
        'PGSSLROOTCERT': '/path/to/root.crt',
        'PGSSLCERT': '/path/to/cert.crt',
        'PGSSLKEY': '/path/to/key.key',
        'PGPASSFILE': '/path/to/passfile'
    }

    args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)
    
    assert args == expected_args
    assert env == expected_env

    # Test with dbname as None and service as None
    settings_dict['NAME'] = None
    settings_dict['OPTIONS']['service'] = None

    expected_args_default_db = [
        'psql',
        '-U', 'test_user',
        '-h', 'localhost',
        '-p', '5432',
        'postgres',
        '--some-param', 'value'
    ]
    
    args_default_db, env_default_db = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

    assert args_default_db == expected_args_default_db
    assert env_default_db == expected_env