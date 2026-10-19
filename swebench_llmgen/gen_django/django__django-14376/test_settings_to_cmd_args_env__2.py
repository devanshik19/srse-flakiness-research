import pytest
from django.db.backends.base.client import BaseDatabaseClient
from django.contrib.auth.models import User

class DatabaseClient(BaseDatabaseClient):
    executable_name = 'mysql'

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
        'PASSWORD': 'secure_password',
        'OPTIONS': {
            'db': 'my_database',
            'user': 'my_user',
            'password': 'my_password',
            'host': 'localhost',
            'port': 3306,
            'ssl': {
                'ca': 'path/to/server_ca.pem',
                'cert': 'path/to/client_cert.pem',
                'key': 'path/to/client_key.pem'
            },
            'charset': 'utf8',
            'read_default_file': 'my.cnf'
        }
    }
    parameters = ['--verbose']

    client = DatabaseClient()
    args, env = client.settings_to_cmd_args_env(settings_dict, parameters)

    assert args == [
        'mysql',
        '--defaults-file=my.cnf',
        '--user=my_user',
        '--host=localhost',
        '--port=3306',
        '--ssl-ca=path/to/server_ca.pem',
        '--ssl-cert=path/to/client_cert.pem',
        '--ssl-key=path/to/client_key.pem',
        '--default-character-set=utf8',
        'my_database',
        '--verbose'
    ]
    assert env == {'MYSQL_PWD': 'my_password'}

    # Test variants for missing values
    settings_dict['OPTIONS'].pop('user')
    args, env = client.settings_to_cmd_args_env(settings_dict, parameters)
    assert '--user=my_user' not in args