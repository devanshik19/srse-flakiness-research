import pytest
from importlib import import_module
from django.apps import apps
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.management.sql import sql_flush
from django.db import connections
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_handle_flush_interactive(mocker):
    # Prepare the database and create a user
    User.objects.create_user(username='testuser', password='testpass')

    # Mock inputs for interactive confirmation
    mock_input = mocker.patch('builtins.input', return_value='yes')
    
    # Capture the connection and settings
    connection = connections[DEFAULT_DB_ALIAS]
    
    # Call the command with interactive flush
    call_command('flush', database=DEFAULT_DB_ALIAS, interactive=True, verbosity=0)
    
    # Check that the database is empty
    assert User.objects.count() == 0

    # Assert that the input was called
    mock_input.assert_called_once()

@pytest.mark.django_db
def test_handle_flush_non_interactive(mocker):
    # Prepare the database and create a user
    User.objects.create_user(username='testuser', password='testpass')

    # Call the command with non-interactive flush
    call_command('flush', database=DEFAULT_DB_ALIAS, interactive=False, verbosity=0)
    
    # Check that the database is empty
    assert User.objects.count() == 0

@pytest.mark.django_db
def test_handle_flush_cancelled(mocker):
    # Prepare the database and create a user
    User.objects.create_user(username='testuser', password='testpass')

    # Mock inputs for interactive confirmation to simulate cancellation
    mock_input = mocker.patch('builtins.input', return_value='no')
    
    # Call the command with interactive flush
    result = call_command('flush', database=DEFAULT_DB_ALIAS, interactive=True, verbosity=0)

    # Check that the user is still present (flush cancelled)
    assert User.objects.count() == 1
    assert "Flush cancelled." in result

@pytest.mark.django_db
def test_handle_flush_execute_error(mocker):
    # Prepare the database and create a user
    User.objects.create_user(username='testuser', password='testpass')
    
    # Mock the execute_sql_flush to raise an exception
    mocker.patch.object(connections[DEFAULT_DB_ALIAS].ops, 'execute_sql_flush', side_effect=Exception("Simulated SQL error"))

    # Call the command and expect a CommandError
    with pytest.raises(CommandError) as excinfo:
        call_command('flush', database=DEFAULT_DB_ALIAS, interactive=False, verbosity=0)

    assert "couldn't be flushed" in str(excinfo.value)