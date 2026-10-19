import sys
import pytest
from django.core.management import CommandError
from django.core.management import ManagementUtility
from django.utils import autoreload
from django.contrib.auth.models import User

def test_execute_help_no_arguments(capfd):
    utility = ManagementUtility(argv=['manage.py'])
    utility.execute()
    captured = capfd.readouterr()
    assert "Usage:" in captured.out

def test_execute_help_with_commands(capfd):
    utility = ManagementUtility(argv=['manage.py', 'help', '--commands'])
    utility.execute()
    captured = capfd.readouterr()
    assert "Available commands:" in captured.out

def test_execute_version(capfd):
    utility = ManagementUtility(argv=['manage.py', 'version'])
    utility.execute()
    captured = capfd.readouterr()
    assert "Django" in captured.out

def test_execute_help_with_subcommand(capfd):
    utility = ManagementUtility(argv=['manage.py', 'migrate', '--help'])
    utility.execute()
    captured = capfd.readouterr()
    assert "Usage:" in captured.out

def test_execute_invalid_subcommand(capfd):
    utility = ManagementUtility(argv=['manage.py', 'invalid_command'])
    with pytest.raises(SystemExit):
        utility.execute()
    captured = capfd.readouterr()
    assert "No such command 'invalid_command'" in captured.err

def test_execute_runserver_without_reload(monkeypatch, capfd):
    # Monkeypatching to simulate the 'runserver' subcommand
    monkeypatch.setattr(ManagementUtility, 'fetch_command', lambda self, subcommand: User)
    monkeypatch.setattr(autoreload, 'check_errors', lambda func: func)
    
    utility = ManagementUtility(argv=['manage.py', 'runserver', '--noreload'])
    utility.execute()
    captured = capfd.readouterr()
    assert "Starting development server" in captured.out