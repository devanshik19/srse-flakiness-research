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

def test_handle_no_app_labels(command, capsys):
    command.handle()
    captured = capsys.readouterr()
    assert "No changes detected" in captured.out

def test_handle_invalid_app_label(command, capsys):
    command.handle('nonexistent_app')
    captured = capsys.readouterr()
    assert "App 'nonexistent_app' could not be found." in captured.err
    assert command.stderr.getvalue()

def test_handle_empty_migration(command, capsys):
    command.handle('auth', empty=True, name='initial')
    assert "No changes detected" in capsys.readouterr().out

def test_handle_merge_without_conflicts(command, capsys):
    # Create a user to have a change
    User.objects.create_user(username='testuser', password='password')
    
    # There should be some changes to detect now
    command.handle('auth', merge=True)
    assert "No conflicts detected to merge." in capsys.readouterr().out

def test_handle_conflicting_migrations(command, capsys):
    # Create conflict condition
    User.objects.create_user(username='testuser_conflict', password='password')
    with pytest.raises(CommandError, match="Conflicting migrations detected"):
        command.handle('auth', merge=False)
    
def test_handle_changes_with_check(command, capsys):
    User.objects.create_user(username='testuser_check', password='password')
    
    command.handle('auth', check_changes=True)
    assert "No changes detected in app 'auth'" in capsys.readouterr().out

def test_handle_exit_code_option(command):
    with pytest.raises(SystemExit) as excinfo:
        command.handle('auth', exit_code=True)
    assert excinfo.value.code == 1

def test_handle_deprecated_exit_option(command, capsys):
    with warnings.catch_warnings(record=True) as w:
        command.handle('auth', exit_code=True)
        assert len(w) == 1
        assert issubclass(w[0].category, RemovedInDjango20Warning)