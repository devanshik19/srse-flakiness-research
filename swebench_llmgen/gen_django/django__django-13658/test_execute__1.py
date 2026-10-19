import sys
import pytest
from django.core.management import ManagementUtility
from django.core.management.base import CommandError
from django.contrib.auth.models import User

def test_execute_with_no_arguments(capsys):
    utility = ManagementUtility(argv=['manage.py'])
    utility.execute()
    captured = capsys.readouterr()
    assert 'help' in captured.out

def test_execute_help_command(capsys):
    utility = ManagementUtility(argv=['manage.py', 'help'])
    utility.execute()
    captured = capsys.readouterr()
    assert 'help' in captured.out

def test_execute_version_command(capsys):
    utility = ManagementUtility(argv=['manage.py', 'version'])
    utility.execute()
    captured = capsys.readouterr()
    assert 'version' in captured.out

def test_execute_runserver_without_reload(capsys):
    utility = ManagementUtility(argv=['manage.py', 'runserver', '--noreload'])
    utility.execute()
    captured = capsys.readouterr()
    assert 'Start the auto-reloading dev server' not in captured.out

def test_execute_fetch_command_invalid(capsys):
    utility = ManagementUtility(argv=['manage.py', 'invalid_subcommand'])
    
    with pytest.raises(SystemExit):
        utility.execute()
    
    captured = capsys.readouterr()
    assert 'invalid_subcommand' in captured.err

def test_execute_with_settings_exception(capsys, settings):
    settings.INSTALLED_APPS = []  # Simulate ImproperlyConfigured
    utility = ManagementUtility(argv=['manage.py'])
    utility.execute()
    captured = capsys.readouterr()
    assert 'ImproperlyConfigured' in captured.err

def test_execute_with_pythonpath(capsys):
    utility = ManagementUtility(argv=['manage.py', '--pythonpath', 'some_path'])
    utility.execute()
    captured = capsys.readouterr()
    assert '--pythonpath' in captured.out

def test_execute_with_user(capsys):
    User.objects.create_user(username='testuser', password='testpass')
    utility = ManagementUtility(argv=['manage.py', 'help'])
    utility.execute()
    captured = capsys.readouterr()
    assert 'testuser' in captured.out  # Check if we can access the User model