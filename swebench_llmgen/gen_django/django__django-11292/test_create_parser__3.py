import pytest
import sys
from django.core.management.base import BaseCommand

class TestBaseCommand(BaseCommand):
    def create_parser(self, prog_name, subcommand, **kwargs):
        return super().create_parser(prog_name, subcommand, **kwargs)

def test_create_parser():
    command = TestBaseCommand(stdout=sys.stdout, stderr=sys.stderr, no_color=False, force_color=False)
    parser = command.create_parser("manage.py", "testcommand")

    # Checking default verbosity argument
    default_verbosity = parser.get_default('verbosity')
    assert default_verbosity == 1

    # Check that help is present
    assert parser.description == command.help

    # Check the presence of version argument
    version_action = parser._actions[-1]
    assert version_action.option_strings == ['--version']

    # Check verbosity options
    verbosity_choices = [0, 1, 2, 3]
    assert all(choice in verbosity_choices for choice in [0, 1, 2, 3])

    # Check settings argument
    settings_arg = next(arg for arg in parser._actions if arg.dest == 'settings')
    assert settings_arg.help == ("The Python path to a settings module, e.g. "
                                  '"myproject.settings.main". If this isn\'t provided, the '
                                  'DJANGO_SETTINGS_MODULE environment variable will be used.')

    # Check pythonpath argument
    pythonpath_arg = next(arg for arg in parser._actions if arg.dest == 'pythonpath')
    assert pythonpath_arg.help == 'A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".'

    # Check traceback argument
    traceback_arg = next(arg for arg in parser._actions if arg.dest == 'traceback')
    assert traceback_arg.help == 'Raise on CommandError exceptions'

    # Check no-color argument
    no_color_arg = next(arg for arg in parser._actions if arg.dest == 'no_color')
    assert no_color_arg.help == "Don't colorize the command output."

    # Check force-color argument
    force_color_arg = next(arg for arg in parser._actions if arg.dest == 'force_color')
    assert force_color_arg.help == 'Force colorization of the command output.'