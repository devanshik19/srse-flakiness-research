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
        'PASSWORD': 'test_password',
        'OPTIONS': {
            'db': 'test_db',
            'user': 'test_user_override',
            'password': 'override_password',
            'host': 'localhost',
            'port': '3306',
            'ssl': {
                'ca': '/path/to/ca.pem',
                'cert': '/path/to/cert.pem',
                'key': '/path/to/key.pem',
            },
            'read_default_file': '/path/to/default.cnf',
            'charset': 'utf8',
        }
    }
    parameters = ['--some-parameter']

    expected_args = [
        'mysql',
        '--defaults-file=/path/to/default.cnf',
        '--user=test_user_override',
        '--host=localhost',
        '--port=3306',
        '--ssl-ca=/path/to/ca.pem',
        '--ssl-cert=/path/to/cert.pem',
        '--ssl-key=/path/to/key.pem',
        '--default-character-set=utf8',
        'test_db',
        '--some-parameter'
    ]
    expected_env = {'MYSQL_PWD': 'override_password'}

    args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

    assert args == expected_args
    assert env == expected_env