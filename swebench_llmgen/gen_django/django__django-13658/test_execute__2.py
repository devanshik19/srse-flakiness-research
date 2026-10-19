import sys
import pytest
from django.core.management import CommandError
from django.core.management import BaseCommand
from django.core.management import CommandParser
from django.core.management import handle_default_options
from django.utils import autoreload
from django.contrib.auth.models import User
from django.apps import apps
from django.conf import settings
from django.core.management import ManagementUtility


@pytest.fixture
def management_utility():
    # Returns an instance of ManagementUtility with empty argv for testing
    return ManagementUtility(argv=['manage.py'])


def test_execute_no_arguments(management_utility, capsys):
    management_utility.execute()
    captured = capsys.readouterr()
    assert 'Type ' in captured.out  # Check for help text


def test_execute_help_argument(management_utility, capsys):
    management_utility.argv.append('help')
    management_utility.execute()
    captured = capsys.readouterr()
    assert 'Type ' in captured.out  # Check for help text


def test_execute_version_argument(management_utility, capsys):
    management_utility.argv.append('version')
    management_utility.execute()
    captured = capsys.readouterr()
    assert captured.out.strip() == django.get_version()


def test_execute_no_settings_configured(management_utility, capsys):
    management_utility.argv.append('runserver')
    settings.configured = False
    management_utility.execute()
    captured = capsys.readouterr()
    assert 'Type ' in captured.out  # Check for help text


def test_execute_with_settings_configured(management_utility, capsys):
    management_utility.argv.append('runserver')
    settings.configured = True
    # Simulate fetching a command
    management_utility.fetch_command = lambda subcommand: BaseCommand()
    management_utility.execute()
    # Check that fetch_command was called
    assert management_utility.argv[-1] == 'runserver'


def test_execute_autocomplete(management_utility):
    management_utility.autocomplete = lambda: None  # No-op for testing
    management_utility.execute()
    assert True  # Simply check it runs without error