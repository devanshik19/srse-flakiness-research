import pytest
from django.core.management import CommandError
from django.core.management.commands.flush import Command
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock

@pytest.fixture
def command():
    return Command()

def test_handle_flush_confirm_yes(command):
    options = {
        'database': 'default',
        'verbosity': 1,
        'interactive': True,
        'reset_sequences': True,
        'allow_cascade': False,
        'inhibit_post_migrate': False
    }

    sql_flush_mock = patch('django.core.management.sql.sql_flush', return_value=['SQL1', 'SQL2']).start()
    execute_sql_flush_mock = patch.object(command, 'connections', new_callable=MagicMock).start()

    with patch('builtins.input', return_value='yes'):
        command.handle(**options)

    sql_flush_mock.assert_called_once()
    execute_sql_flush_mock.return_value.ops.execute_sql_flush.assert_called_once_with(
        options['database'], ['SQL1', 'SQL2']
    )

@pytest.mark.parametrize("interactive, expected_input", [
    (True, 'yes'),
    (False, 'yes'),
])
def test_handle_flush_confirm_no(command, interactive, expected_input):
    options = {
        'database': 'default',
        'verbosity': 1,
        'interactive': interactive,
        'reset_sequences': True,
        'allow_cascade': False,
        'inhibit_post_migrate': False
    }

    with patch('django.core.management.sql.sql_flush', return_value=['SQL1']):
        with patch('builtins.input', return_value='no'):
            with pytest.raises(SystemExit):
                command.handle(**options)

def test_handle_flush_execute_sql_error(command):
    options = {
        'database': 'default',
        'verbosity': 1,
        'interactive': True,
        'reset_sequences': True,
        'allow_cascade': False,
        'inhibit_post_migrate': False
    }

    sql_flush_mock = patch('django.core.management.sql.sql_flush', return_value=['SQL1']).start()
    execute_sql_flush_mock = patch.object(command, 'connections', new_callable=MagicMock).start()
    
    execute_sql_flush_mock.return_value.ops.execute_sql_flush.side_effect = Exception("SQL Error")

    with patch('builtins.input', return_value='yes'):
        with pytest.raises(CommandError):
            command.handle(**options)

def test_handle_empty_sql(command):
    options = {
        'database': 'default',
        'verbosity': 1,
        'interactive': True,
        'reset_sequences': True,
        'allow_cascade': False,
        'inhibit_post_migrate': True
    }

    with patch('django.core.management.sql.sql_flush', return_value=[]):
        with patch('builtins.input', return_value='yes'):
            command.handle(**options)