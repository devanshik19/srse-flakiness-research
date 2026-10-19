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

@pytest.mark.parametrize("settings_dict, parameters, expected_args, expected_env", [
    ({
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_pass',
        'OPTIONS': {
            'db': 'test_db',
            'user': 'test_user',
            'password': 'test_pass',
            'host': 'localhost',
            'port': '3306',
            'ssl': {},
            'charset': 'utf8mb4',
        }
    }, [], 
    ['mysql', '--user=test_user', '--password=test_pass', '--host=localhost', '--port=3306', 'test_db'], 
    {'MYSQL_PWD': 'test_pass'}),
    
    ({
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_pass',
        'OPTIONS': {
            'db': 'test_db',
            'user': 'test_user',
            'host': '/var/run/mysqld/mysqld.sock',
            'ssl': {},
        }
    }, ['--verbose'], 
    ['mysql', '--user=test_user', '--socket=/var/run/mysqld/mysqld.sock', 'test_db', '--verbose'], 
    {'MYSQL_PWD': 'test_pass'}),

    ({
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_pass',
        'OPTIONS': {
            'host': 'localhost',
            'ssl': {
                'ca': '/path/to/ca.pem',
                'cert': '/path/to/client-cert.pem',
                'key': '/path/to/client-key.pem',
            }
        }
    }, [], 
    ['mysql', '--user=test_user', '--host=localhost', '--ssl-ca=/path/to/ca.pem', '--ssl-cert=/path/to/client-cert.pem', '--ssl-key=/path/to/client-key.pem', 'test_db'], 
    {'MYSQL_PWD': 'test_pass'}),
    
    ({
        'NAME': 'test_db',
        'USER': 'test_user',
        'OPTIONS': {
            'read_default_file': '/path/to/my.cnf',
        }
    }, [], 
    ['mysql', '--defaults-file=/path/to/my.cnf', 'test_db'], 
    None)
])
def test_settings_to_cmd_args_env(settings_dict, parameters, expected_args, expected_env):
    db_client = DatabaseClient()
    args, env = db_client.settings_to_cmd_args_env(settings_dict, parameters)
    
    assert args == expected_args
    assert env == expected_env