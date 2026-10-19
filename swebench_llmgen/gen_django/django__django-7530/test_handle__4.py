import io
import os
import sys
import warnings
import pytest
from django.apps import apps
from django.core.management import CommandError
from django.core.management.commands.makemigrations import Command
from django.contrib.auth.models import User

@pytest.fixture
def command():
    return Command()

def test_handle_no_changes(command, capsys):
    command.handle('auth', verbosity=1)  # no changes in the auth app
    captured = capsys.readouterr()
    assert "No changes detected in apps 'auth'" in captured.out

def test_handle_app_not_found(command, capsys):
    command.handle('nonexistent_app')
    captured = capsys.readouterr()
    assert "App 'nonexistent_app' could not be found. Is it in INSTALLED_APPS?" in captured.err
    assert sys.exit(2) is None  # Validate exit

def test_handle_with_conflicting_migrations(command):
    User.objects.create(username='testuser')  # Create user model to ensure migration exists
    command.handle('auth', merge=False)  # Should raise CommandError due to conflicts
    with pytest.raises(CommandError):
        command.handle('auth', merge=False)

def test_handle_empty_migration(command, capsys):
    command.handle('auth', empty=True, name='test_empty_migration')
    captured = capsys.readouterr()
    assert "No conflicts detected to merge." in captured.out

def test_handle_with_exit_code(command, capsys):
    command.exit_code = True
    command.handle('auth', verbosity=1)
    captured = capsys.readouterr()
    assert "No changes detected in apps 'auth'" in captured.out
    assert sys.exit(1) is None  # Validate exit

def test_handle_with_check_changes(command):
    command.handle('auth', check_changes=True)
    assert sys.exit(1) is None  # Validate exit for check_changes case