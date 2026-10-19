import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.contrib.auth.models import User
from django.db import connections

@pytest.fixture
def create_user():
    return User.objects.create_user(username='testuser', password='testpass')

def test_handle_flush_confirm(create_user):
    database = DEFAULT_DB_ALIAS
    options = {
        'database': database,
        'verbosity': 2,
        'interactive': False,
    }
    
    # Ensure that the user is created
    assert User.objects.count() == 1
    
    # Here we flush the database
    call_command('flush', database=database, verbosity=0, interactive=False)
    
    # Check that the user is deleted after flush
    assert User.objects.count() == 0

def test_handle_flush_interactive_confirm(create_user, monkeypatch):
    database = DEFAULT_DB_ALIAS
    options = {
        'database': database,
        'verbosity': 2,
        'interactive': True,
    }

    # Ensure that the user is created
    assert User.objects.count() == 1
    
    # Simulate user confirmation
    monkeypatch.setattr('builtins.input', lambda _: 'yes')
    
    # Flush the database
    call_command('flush', database=database, verbosity=0, interactive=True)
    
    # Check that the user is deleted after flush
    assert User.objects.count() == 0

def test_handle_flush_cancel(create_user, monkeypatch):
    database = DEFAULT_DB_ALIAS
    options = {
        'database': database,
        'verbosity': 2,
        'interactive': True,
    }
    
    assert User.objects.count() == 1
    
    # Simulate user cancellation
    monkeypatch.setattr('builtins.input', lambda _: 'no')
    
    # Attempt to flush the database
    call_command('flush', database=database, verbosity=0, interactive=True)
    
    # Check that the user still exists
    assert User.objects.count() == 1

def test_handle_flush_database_error(create_user, monkeypatch):
    database = "non_existent_db"
    options = {
        'database': database,
        'verbosity': 2,
        'interactive': False,
    }
    
    with pytest.raises(CommandError):
        call_command('flush', database=database, verbosity=0, interactive=False)