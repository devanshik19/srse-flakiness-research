import pytest
from django.core.management import call_command
from django.contrib.auth.models import User
from django.core.management.base import CommandError
from django.db import connections

def test_handle_flush_database(monkeypatch):
    # Prepare the test database by creating a user
    User.objects.create_user(username='testuser', password='testpass')

    # Capture input() calls
    monkeypatch.setattr('builtins.input', lambda prompt: 'yes')

    # Call the flush command with options
    call_command('flush', database='default', interactive=True)

    # Ensure the database is empty
    assert User.objects.count() == 0

def test_handle_flush_abort(monkeypatch):
    # Prepare the test database by creating a user
    User.objects.create_user(username='testuser', password='testpass')

    # Simulate user input for aborting flush
    monkeypatch.setattr('builtins.input', lambda prompt: 'no')

    # Call the flush command with options
    call_command('flush', database='default', interactive=True)

    # Ensure the database is still populated
    assert User.objects.count() == 1

def test_handle_flush_with_reset_sequences_and_cascade(monkeypatch):
    User.objects.create_user(username='testuser', password='testpass')
    
    monkeypatch.setattr('builtins.input', lambda prompt: 'yes')
    
    # Call the flush command with reset_sequences and allow_cascade
    call_command('flush', database='default', interactive=True,
                 reset_sequences=True, allow_cascade=True)

    # Ensure the database is empty
    assert User.objects.count() == 0

def test_handle_flush_with_no_tables(monkeypatch):
    from django.core.management import call_command

    monkeypatch.setattr('builtins.input', lambda prompt: 'yes')

    # Call the flush command on a non-existing database
    with pytest.raises(CommandError):
        call_command('flush', database='nonexistent_db', interactive=True)