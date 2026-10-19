import pytest
from django.core.management import CommandError
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db import connection

def test_handle_flush():
    # Create a user to flush
    User.objects.create(username="testuser", password="testpass")

    # Check initial state
    assert User.objects.count() == 1

    # Execute command with various options
    options = {
        'database': DEFAULT_DB_ALIAS,
        'verbosity': 1,
        'interactive': False,
        'reset_sequences': True,
        'allow_cascade': False,
        'inhibit_post_migrate': False,
    }

    call_command('flush', **options)

    # Check if the user is flushed
    assert User.objects.count() == 0

def test_handle_interactive_flush():
    User.objects.create(username="testuser", password="testpass")
    assert User.objects.count() == 1

    # Simulate interactive input
    options = {
        'database': DEFAULT_DB_ALIAS,
        'verbosity': 1,
        'interactive': True,
        'reset_sequences': True,
        'allow_cascade': False,
        'inhibit_post_migrate': False,
    }

    with pytest.raises(EOFError):
        call_command('flush', **options)

    assert User.objects.count() == 1  # Ensure user still exists after cancel

def test_handle_flush_with_sql_error():
    options = {
        'database': 'non_existent_db',
        'verbosity': 1,
        'interactive': False,
        'reset_sequences': True,
        'allow_cascade': False,
        'inhibit_post_migrate': False,
    }

    with pytest.raises(CommandError) as e:
        call_command('flush', **options)

    assert "couldn't be flushed" in str(e.value)