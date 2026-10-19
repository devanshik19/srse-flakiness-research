import sys
import pytest
from django.core.management import ManagementUtility
from django.core.management.base import CommandError
from django.contrib.auth.models import User

def test_execute_help_without_arguments(capfd):
    utility = ManagementUtility(argv=['manage.py'])
    utility.execute()
    captured = capfd.readouterr()
    assert 'Usage:' in captured.out  # Check if help text is displayed

def test_execute_help_with_commands_argument(capfd):
    utility = ManagementUtility(argv=['manage.py', 'help', '--commands'])
    utility.execute()
    captured = capfd.readouterr()
    assert 'Available commands' in captured.out  # Check if commands list is displayed

def test_execute_version(capfd):
    utility = ManagementUtility(argv=['manage.py', 'version'])
    utility.execute()
    captured = capfd.readouterr()
    assert django.get_version() in captured.out  # Check if version is displayed

def test_execute_help_with_subcommand(capfd):
    utility = ManagementUtility(argv=['manage.py', 'help', 'migrate'])
    utility.execute()
    captured = capfd.readouterr()
    assert 'Usage: manage.py migrate' in captured.out  # Check if migrate command help is displayed

def test_execute_runserver(capfd):
    utility = ManagementUtility(argv=['manage.py', 'runserver'])
    utility.execute()
    # The stdout capture can vary, but we want to ensure no exception was raised
    captured = capfd.readouterr()
    assert 'Starting development server' in captured.out  # This text may vary based on implementation

def test_execute_invalid_subcommand(capfd):
    utility = ManagementUtility(argv=['manage.py', 'invalid_command'])
    with pytest.raises(SystemExit):  # expecting SystemExit from invalid command
        utility.execute()
    captured = capfd.readouterr()
    assert 'Unknown command' in captured.out  # Check if unknown command error is displayed

def test_execute_with_settings(capfd):
    utility = ManagementUtility(argv=['manage.py', '--settings=my_project.settings'])
    utility.execute()
    captured = capfd.readouterr()
    assert 'My Project' in captured.out  # Check if project-specific output is displayed (customize as needed)