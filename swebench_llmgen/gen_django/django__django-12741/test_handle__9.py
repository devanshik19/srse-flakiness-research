import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import connections, DEFAULT_DB_ALIAS

@pytest.mark.django_db
def test_handle_flush_interactive_cancel():
    # Creating a user instance to ensure the database has some content
    User.objects.create_user(username='testuser', password='testpass')

    command = call_command('flush', interactive=True, database=DEFAULT_DB_ALIAS, verbosity=0)

    # Simulating user input to cancel the operation
    with pytest.raises(SystemExit):
        command.handle(database=DEFAULT_DB_ALIAS, interactive=True, confirm='no')

    # Ensure user still exists
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_handle_flush_interactive_confirm():
    # Creating a user instance to ensure the database has some content
    User.objects.create_user(username='testuser', password='testpass')

    # Here we simulate a flush and confirm. 
    import builtins
    original_input = builtins.input
    builtins.input = lambda _: 'yes'  # Simulate user typing 'yes'

    try:
        call_command('flush', interactive=True, database=DEFAULT_DB_ALIAS)
        # Ensure user was flushed from the database
        assert User.objects.count() == 0
    finally:
        builtins.input = original_input  # Restore original input function

@pytest.mark.django_db
def test_handle_flush_no_interactive():
    User.objects.create_user(username='testuser', password='testpass')

    call_command('flush', interactive=False, database=DEFAULT_DB_ALIAS)

    # Check that user was flushed
    assert User.objects.count() == 0

@pytest.mark.django_db
def test_handle_flush_with_exception():
    User.objects.create_user(username='testuser', password='testpass')

    connection = connections[DEFAULT_DB_ALIAS]
    # Simulating an exception during the flush
    original_execute_sql_flush = connection.ops.execute_sql_flush
    def raise_exception(database, sql_list):
        raise Exception("Forced Exception during flush")

    connection.ops.execute_sql_flush = raise_exception

    with pytest.raises(CommandError, match="Database %s couldn't be flushed." % connection.settings_dict['NAME']):
        call_command('flush', database=DEFAULT_DB_ALIAS)
    
    connection.ops.execute_sql_flush = original_execute_sql_flush  # Restore original method