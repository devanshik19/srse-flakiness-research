import pytest
from django.core.management import CommandError
from django.contrib.auth.models import User
from django.core.management.commands.flush import Command

@pytest.mark.django_db
def test_handle_flush():
    # Create a user to have some data in the database
    User.objects.create_user(username='testuser', password='password')

    command = Command()
    
    # Test flush with interactive confirmation
    options = {
        'database': DEFAULT_DB_ALIAS,
        'verbosity': 1,
        'interactive': True,
        'reset_sequences': True,
        'allow_cascade': False,
        'inhibit_post_migrate': False
    }
    
    # Patch the input to simulate user input
    import builtins
    original_input = builtins.input
    builtins.input = lambda prompt: 'yes'

    try:
        command.handle(**options)

        # Check that the user is deleted after flush
        assert User.objects.count() == 0
    finally:
        # Restore input
        builtins.input = original_input

@pytest.mark.django_db
def test_handle_flush_cancelled():
    User.objects.create_user(username='testuser', password='password')

    command = Command()
    
    # Test flush with non-interactive confirmation
    options = {
        'database': DEFAULT_DB_ALIAS,
        'verbosity': 1,
        'interactive': False,
        'reset_sequences': True,
        'allow_cascade': False,
        'inhibit_post_migrate': False
    }
    
    command.handle(**options)

    # Check that the user still exists after non-interactive flush
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_handle_flush_error():
    command = Command()
    
    # Test flush with a database that will cause an error
    options = {
        'database': 'non_existent_database',
        'verbosity': 1,
        'interactive': True,
        'reset_sequences': True,
        'allow_cascade': False,
        'inhibit_post_migrate': False
    }
    
    with pytest.raises(CommandError):
        command.handle(**options)