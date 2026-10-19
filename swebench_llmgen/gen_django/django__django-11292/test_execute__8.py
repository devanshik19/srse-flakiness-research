import pytest
from django.core.management.base import BaseCommand
from django.core.management import CommandError
from django.contrib.auth.models import User
from io import StringIO

class TestBaseCommand(BaseCommand):
    def __init__(self):
        super().__init__(stdout=StringIO(), stderr=StringIO(), no_color=False, force_color=False)

    def handle(self, *args, **options):
        return "Command executed"

def test_execute_with_valid_options():
    command = TestBaseCommand()
    options = {
        'force_color': False,
        'no_color': False,
        'skip_checks': False,
    }
    output = command.execute("arg1", "arg2", **options)
    assert output == "Command executed"
    assert command.stdout.getvalue() == "Command executed\n"

def test_execute_with_force_color():
    command = TestBaseCommand()
    command.style = None  # Initializing style manually for test
    options = {
        'force_color': True,
        'no_color': False,
        'skip_checks': False,
    }
    output = command.execute("arg1", "arg2", **options)
    assert output == "Command executed"

def test_execute_with_no_color():
    command = TestBaseCommand()
    command.style = None  # Initializing style manually for test
    options = {
        'force_color': False,
        'no_color': True,
        'skip_checks': False,
    }
    output = command.execute("arg1", "arg2", **options)
    assert output == "Command executed"

def test_execute_with_force_and_no_color():
    command = TestBaseCommand()
    options = {
        'force_color': True,
        'no_color': True,
        'skip_checks': False,
    }
    with pytest.raises(CommandError, match="The --no-color and --force-color options can't be used together."):
        command.execute("arg1", "arg2", **options)

def test_execute_with_system_checks_skipped():
    command = TestBaseCommand()
    command.requires_system_checks = True
    options = {
        'force_color': False,
        'no_color': False,
        'skip_checks': True,
    }
    output = command.execute("arg1", "arg2", **options)
    assert output == "Command executed"