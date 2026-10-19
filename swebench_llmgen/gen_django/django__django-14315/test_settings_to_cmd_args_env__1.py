import pytest
from django.db.backends.postgresql.client import DatabaseClient

def test_settings_to_cmd_args_env():
    # Prepare test data
    settings_dict = {
        'HOST': 'localhost',
        'PORT': 5432,
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_pass',
        'OPTIONS': {
            'passfile': 'test_passfile',
            'service': 'test_service',
            'sslmode': 'require',
            'sslrootcert': 'test_sslrootcert',
            'sslcert': 'test_sslcert',
            'sslkey': 'test_sslkey',
        }
    }
    parameters = ['--some-parameter']

    # Assign executable_name for testing purposes
    DatabaseClient.executable_name = 'psql'

    # Call the method
    args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

    # Assertions
    assert args == [
        'psql', 
        '-U', 'test_user',
        '-h', 'localhost',
        '-p', '5432', 
        'test_db', 
        '--some-parameter'
    ]
    
    assert env == {
        'PGPASSWORD': 'test_pass',
        'PGSERVICE': 'test_service',
        'PGSSLMODE': 'require',
        'PGSSLROOTCERT': 'test_sslrootcert',
        'PGSSLCERT': 'test_sslcert',
        'PGSSLKEY': 'test_sslkey',
        'PGPASSFILE': 'test_passfile'
    }

    # Test when dbname and service are not provided
    settings_dict_no_db_service = {
        'HOST': 'localhost',
        'PORT': 5432,
        'OPTIONS': {}
    }
    
    args_no_db_service, env_no_db_service = DatabaseClient.settings_to_cmd_args_env(settings_dict_no_db_service, parameters)
    
    assert args_no_db_service == [
        'psql',
        '-h', 'localhost',
        '-p', '5432',
        'postgres',
        '--some-parameter'
    ]
    assert env_no_db_service == {}