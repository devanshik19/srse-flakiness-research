import pytest
from django.core.management.base import BaseCommand
from django.core.management import CommandError
from django.contrib.auth.models import User
from io import StringIO

class TestBaseCommand(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        self.stdout = stdout or StringIO()
        self.stderr = stderr or StringIO()
        self.no_color = no_color
        self.force_color = force_color
        self.requires_system_checks = True
        self.requires_migrations_checks = False
        self.output_transaction = False

    def handle(self, *args, **options):
        return "Command executed successfully."

def test_execute_success():
    command = TestBaseCommand()
    options = {
        'force_color': False,
        'no_color': False,
        'skip_checks': False,
        'stdout': StringIO(),
        'stderr': StringIO(),
    }

    output = command.execute('arg1', 'arg2', **options)
    assert output == "Command executed successfully."
    assert command.stdout.getvalue() == ""

def test_execute_with_force_color():
    command = TestBaseCommand()
    options = {
        'force_color': True,
        'no_color': False,
        'skip_checks': False,
        'stdout': StringIO(),
        'stderr': StringIO(),
    }
    
    command.execute('arg1', 'arg2', **options)
    assert command.style == color_style(force_color=True)

def test_execute_with_no_color():
    command = TestBaseCommand()
    options = {
        'force_color': False,
        'no_color': True,
        'skip_checks': False,
        'stdout': StringIO(),
        'stderr': StringIO(),
    }

    command.execute('arg1', 'arg2', **options)
    assert command.style is None

def test_execute_with_conflicting_color_options():
    command = TestBaseCommand()
    options = {
        'force_color': True,
        'no_color': True,
        'skip_checks': False,
    }

    with pytest.raises(CommandError, match="The --no-color and --force-color options can't be used together."):
        command.execute('arg1', 'arg2', **options)

def test_execute_skip_checks():
    command = TestBaseCommand()
    options = {
        'force_color': False,
        'no_color': False,
        'skip_checks': True,
        'stdout': StringIO(),
        'stderr': StringIO(),
    }

    output = command.execute('arg1', 'arg2', **options)
    assert output == "Command executed successfully."