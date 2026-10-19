import pytest
from django.db.backends.base.client import BaseDatabaseClient
from django.contrib.auth.models import User

class DatabaseClient(BaseDatabaseClient):
    executable_name = 'mysql'

    @classmethod
    def settings_to_cmd_args_env(cls, settings_dict, parameters):
        args = [cls.executable_name]
        env = None
        db = settings_dict['OPTIONS'].get('db', settings_dict['NAME'])
        user = settings_dict['OPTIONS'].get('user', settings_dict['USER'])
        password = settings_dict['OPTIONS'].get(
            'password',
            settings_dict['OPTIONS'].get('passwd', settings_dict['PASSWORD'])
        )
        host = settings_dict['OPTIONS'].get('host', settings_dict['HOST'])
        port = settings_dict['OPTIONS'].get('port', settings_dict['PORT'])
        server_ca = settings_dict['OPTIONS'].get('ssl', {}).get('ca')
        client_cert = settings_dict['OPTIONS'].get('ssl', {}).get('cert')
        client_key = settings_dict['OPTIONS'].get('ssl', {}).get('key')
        defaults_file = settings_dict['OPTIONS'].get('read_default_file')
        charset = settings_dict['OPTIONS'].get('charset')

        if defaults_file:
            args += ["--defaults-file=%s" % defaults_file]
        if user:
            args += ["--user=%s" % user]
        if password:
            env = {'MYSQL_PWD': password}
        if host:
            if '/' in host:
                args += ["--socket=%s" % host]
            else:
                args += ["--host=%s" % host]
        if port:
            args += ["--port=%s" % port]
        if server_ca:
            args += ["--ssl-ca=%s" % server_ca]
        if client_cert:
            args += ["--ssl-cert=%s" % client_cert]
        if client_key:
            args += ["--ssl-key=%s" % client_key]
        if charset:
            args += ['--default-character-set=%s' % charset]
        if db:
            args += [db]
        args.extend(parameters)
        return args, env


def test_settings_to_cmd_args_env():
    settings_dict = {
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_pass',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'db': 'test_database',
            'user': 'test_user_option',
            'password': 'test_pass_option',
            'host': 'test_host',
            'port': '1234',
            'ssl': {
                'ca': 'path/to/ca.pem',
                'cert': 'path/to/cert.pem',
                'key': 'path/to/key.pem',
            },
            'charset': 'utf8mb4',
            'read_default_file': '/path/to/my.cnf'
        }
    }
    parameters = ['--additional-param']
    
    args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

    assert args == [
        'mysql',
        '--defaults-file=/path/to/my.cnf',
        '--user=test_user_option',
        '--host=test_host',
        '--port=1234',
        '--ssl-ca=path/to/ca.pem',
        '--ssl-cert=path/to/cert.pem',
        '--ssl-key=path/to/key.pem',
        '--default-character-set=utf8mb4',
        'test_database',
        '--additional-param'
    ]
    assert env == {'MYSQL_PWD': 'test_pass_option'}

    # Test with minimum options
    minimal_settings_dict = {
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_pass',
        'OPTIONS': {}
    }

    args_min, env_min = DatabaseClient.settings_to_cmd_args_env(minimal_settings_dict, [])
    
    assert args_min == ['mysql', 'test_db']
    assert env_min is None