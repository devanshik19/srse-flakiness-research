import pytest
from django.core.management import ManagementUtility
from django.conf import settings
from django.core.management.base import CommandError
from django.contrib.auth.models import User
import sys

def test_execute_help_without_arguments(capfd):
    utility = ManagementUtility(argv=['manage.py'])
    utility.execute()
    captured = capfd.readouterr()
    assert 'Type ' in captured.out  # Check if help text was printed

def test_execute_help_with_commands_option(capfd):
    utility = ManagementUtility(argv=['manage.py', 'help', '--commands'])
    utility.execute()
    captured = capfd.readouterr()
    assert 'Available commands' in captured.out  # Check if commands help text was printed

def test_execute_version(capfd):
    utility = ManagementUtility(argv=['manage.py', 'version'])
    utility.execute()
    captured = capfd.readouterr()
    assert settings.VERSION in captured.out  # Check if version is printed

def test_execute_help_for_specific_command(capfd):
    utility = ManagementUtility(argv=['manage.py', 'migrate', '--help'])
    utility.execute()
    captured = capfd.readouterr()
    assert 'usage' in captured.out  # Check if help for the command was printed

def test_execute_invalid_subcommand(capfd):
    utility = ManagementUtility(argv=['manage.py', 'invalid_command'])
    utility.execute()
    captured = capfd.readouterr()
    assert 'command not found' in captured.out  # Check error message for invalid command

def test_execute_subcommand_runserver(capfd):
    utility = ManagementUtility(argv=['manage.py', 'runserver'])
    utility.execute()
    captured = capfd.readouterr()
    assert 'Starting development server' in captured.out  # Check if runserver started message is in output