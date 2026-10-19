import pytest
import sys
from django.core.management import ManagementUtility

def test_execute_no_arguments(capfd):
    utility = ManagementUtility(argv=['manage.py'])
    utility.execute()
    captured = capfd.readouterr()
    assert 'Usage:' in captured.out  # Check that help is displayed

def test_execute_help_argument(capfd):
    utility = ManagementUtility(argv=['manage.py', 'help'])
    utility.execute()
    captured = capfd.readouterr()
    assert 'Usage:' in captured.out  # Ensure help is shown

def test_execute_version_argument(capfd):
    utility = ManagementUtility(argv=['manage.py', '--version'])
    utility.execute()
    captured = capfd.readouterr()
    assert 'Django:' in captured.out  # Check Django version is printed

def test_execute_invalid_subcommand(capfd):
    utility = ManagementUtility(argv=['manage.py', 'invalid_command'])
    with pytest.raises(SystemExit):
        utility.execute()
    captured = capfd.readouterr()
    assert 'invalid_command' in captured.out  # Ensure invalid command output

def test_execute_settings_exception(capfd):
    utility = ManagementUtility(argv=['manage.py'])
    # Simulate settings being improperly configured
    utility.settings_exception = Exception("Settings error")
    utility.execute()
    captured = capfd.readouterr()
    assert 'Settings error' in captured.out  # Check for settings error handling

def test_execute_autocomplete_called(mocker):
    utility = ManagementUtility(argv=['manage.py', 'runserver'])
    mock_autocomplete = mocker.patch.object(utility, 'autocomplete', return_value=None)
    utility.execute()
    mock_autocomplete.assert_called_once()  # Ensure autocomplete is called

def test_execute_runserver_noreload(capfd):
    utility = ManagementUtility(argv=['manage.py', 'runserver', '--noreload'])
    utility.execute()
    captured = capfd.readouterr()
    assert 'Running development server' in captured.out  # Check runserver output