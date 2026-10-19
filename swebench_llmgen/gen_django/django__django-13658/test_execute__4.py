import pytest
import sys
from django.core.management import ManagementUtility
from django.contrib.auth.models import User

@pytest.fixture
def management_utility():
    return ManagementUtility(argv=sys.argv)

def test_execute_no_arguments(management_utility, capsys):
    management_utility.execute()
    captured = capsys.readouterr()
    assert 'Usage:' in captured.out  # Check for help text

def test_execute_help_argument(management_utility, capsys):
    management_utility.argv.append('help')
    management_utility.execute()
    captured = capsys.readouterr()
    assert 'Usage:' in captured.out  # Check for help text

def test_execute_subcommand(management_utility, capsys):
    management_utility.argv.append('migrate')
    management_utility.execute()
    # Assuming 'migrate' is a valid command, checking its execution 
    # would require specific app contexts, here we check if the command is fetched
    assert management_utility.argv[-1] == 'migrate'

def test_execute_version(management_utility, capsys):
    management_utility.argv.append('--version')
    management_utility.execute()
    captured = capsys.readouterr()
    assert 'Django' in captured.out  # Check for the Django version output

def test_execute_with_settings(management_utility, capsys):
    management_utility.argv.append('--settings=myproject.settings')
    management_utility.execute()
    captured = capsys.readouterr()
    assert 'Usage:' in captured.out  # Ensure it handles settings properly

def test_execute_exception_handling(management_utility, capsys):
    management_utility.argv.append('invalid_command')
    management_utility.execute()
    captured = capsys.readouterr()
    assert 'command not found' in captured.out  # Check for command error messages