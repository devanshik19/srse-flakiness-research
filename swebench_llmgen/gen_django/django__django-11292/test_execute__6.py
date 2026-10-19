import pytest
from django.core.management.base import BaseCommand
from django.core.management import CommandError
from io import StringIO
from django.contrib.auth.models import User

class TestBaseCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        self.stdout = StringIO()
        self.stderr = StringIO()
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        return "Handled"

@pytest.fixture
def command():
    return TestBaseCommand()

def test_execute_with_force_color(command):
    options = {'force_color': True, 'no_color': False}
    command.execute(options=options)
    assert command.style is not None

def test_execute_with_no_color(command):
    options = {'force_color': False, 'no_color': True}
    command.execute(options=options)
    assert command.stderr.style_func is None

def test_execute_with_both_color_options(command):
    options = {'force_color': True, 'no_color': True}
    with pytest.raises(CommandError, match="The --no-color and --force-color options can't be used together."):
        command.execute(options=options)

def test_execute_skips_system_checks(command):
    command.requires_system_checks = True
    options = {'skip_checks': True}
    output = command.execute(options=options)
    assert output == "Handled"

def test_execute_performs_system_checks(command):
    command.requires_system_checks = True
    options = {'skip_checks': False}
    with pytest.raises(Exception):
        command.check()  # Assuming check will raise if not properly configured
    command.execute(options=options)

def test_execute_produces_output(command):
    options = {'force_color': True}
    output = command.execute(options=options)
    assert output == "Handled"
    assert command.stdout.getvalue() == "Handled\n"