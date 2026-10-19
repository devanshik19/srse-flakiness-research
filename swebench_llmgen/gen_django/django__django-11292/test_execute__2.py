import pytest
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from io import StringIO

class TestBaseCommand(BaseCommand):
    def __init__(self, **options):
        self.stdout = StringIO()
        self.stderr = StringIO()
        self.no_color = options.get('no_color', False)
        self.force_color = options.get('force_color', False)
        self.requires_system_checks = True
        self.requires_migrations_checks = False
        self.output_transaction = False

    def handle(self, *args, **options):
        return "Command executed"

def test_execute_no_color_force_color():
    command = TestBaseCommand()
    options = {
        'force_color': True,
        'no_color': True,
        'skip_checks': True,
    }
    with pytest.raises(CommandError, match="The --no-color and --force-color options can't be used together."):
        command.execute([], options)

def test_execute_force_color():
    command = TestBaseCommand()
    options = {
        'force_color': True,
        'no_color': False,
    }
    command.execute([], options)
    assert command.style is not None

def test_execute_no_color():
    command = TestBaseCommand()
    options = {
        'force_color': False,
        'no_color': True,
    }
    command.execute([], options)
    assert command.style is None

def test_execute_with_stdout():
    command = TestBaseCommand()
    options = {
        'force_color': False,
        'no_color': False,
        'stdout': StringIO(),
    }
    command.execute([], options)
    assert command.stdout.getvalue() == "Command executed\n"

def test_execute_skip_checks():
    command = TestBaseCommand()
    options = {
        'skip_checks': True,
    }
    output = command.execute([], options)
    assert output == "Command executed"

def test_execute_with_output_transaction():
    command = TestBaseCommand(output_transaction=True)
    options = {
        'database': 'default',
    }
    output = command.execute([], options)
    assert output == "Command executed"