import os
import pytest
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Test command"

    def get_version(self):
        return "1.0.0"

    def add_arguments(self, parser):
        parser.add_argument('--test-arg', help='A test argument')

@pytest.mark.parametrize(
    "prog_name, subcommand, expected_prog, expected_description",
    [
        ("/path/to/manage.py", "test_command", "manage.py test_command", None),
        ("/another/path/manage.py", "runserver", "manage.py runserver", None),
    ]
)
def test_create_parser(prog_name, subcommand, expected_prog, expected_description):
    command = Command(stdout=None, stderr=None, no_color=False, force_color=False)
    parser = command.create_parser(prog_name, subcommand)

    assert parser.prog == expected_prog
    assert parser.description == expected_description

    # Check for presence of expected arguments
    assert any(arg.dest == 'version' for arg in parser._actions)
    assert any(arg.dest == 'verbosity' for arg in parser._actions)
    assert any(arg.dest == 'settings' for arg in parser._actions)
    assert any(arg.dest == 'pythonpath' for arg in parser._actions)
    assert any(arg.dest == 'traceback' for arg in parser._actions)
    assert any(arg.dest == 'no_color' for arg in parser._actions)
    assert any(arg.dest == 'force_color' for arg in parser._actions)
    assert any(arg.dest == 'test_arg' for arg in parser._actions)  # Check custom argument

    # Check default values
    default_verbosity_arg = next(arg for arg in parser._actions if arg.dest == 'verbosity')
    assert default_verbosity_arg.default == 1