import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import connections

@pytest.mark.parametrize("interactive,expected_message", [
    (True, "You have requested a flush of the database."),
    (False, "Flush cancelled.")
])
def test_handle_flush(interactive, expected_message, monkeypatch):
    # Create a User instance to ensure there is data in the database
    User.objects.create(username='testuser')

    # Mock input to simulate confirmation
    if interactive:
        monkeypatch.setattr('builtins.input', lambda _: 'yes')
    else:
        monkeypatch.setattr('builtins.input', lambda _: 'no')

    database = 'default'
    options = {
        'database': database,
        'verbosity': 1,
        'interactive': interactive,
        'reset_sequences': True,
        'allow_cascade': False,
        'inhibit_post_migrate': False
    }

    if interactive:
        # Expect successful flush if confirmed
        assert User.objects.count() == 1
        call_command('flush', **options)
        assert User.objects.count() == 0
    else:
        # Ensure it does not flush if cancelled
        call_command('flush', **options)
        assert User.objects.count() == 1

def test_handle_flush_with_error(monkeypatch):
    # Simulate a database error by breaking the connection
    def broken_execute_sql_flush(database, sql_list):
        raise Exception("Database connection error")

    monkeypatch.setattr(connections['default'].ops, 'execute_sql_flush', broken_execute_sql_flush)
    monkeypatch.setattr('builtins.input', lambda _: 'yes')
    
    with pytest.raises(CommandError, match="couldn't be flushed"):
        call_command('flush', database='default', verbosity=1, interactive=True)