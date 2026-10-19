import os
import pytest
from django.core.management import CommandParser
from django.core.management.base import BaseCommand

class TestBaseCommand(BaseCommand):
    
    def __init__(self):
        super().__init__(stdout=None, stderr=None, no_color=False, force_color=False)
        self.help = "Test command help"
        self._called_from_command_line = True

    def get_version(self):
        return "1.0.0"

    def add_arguments(self, parser):
        parser.add_argument('--custom-arg', help='A custom argument for testing purposes.')

def test_create_parser():
    command = TestBaseCommand()
    prog_name = 'manage.py'
    subcommand = 'testcommand'

    parser = command.create_parser(prog_name, subcommand)

    # Check if the parser was created correctly
    assert isinstance(parser, CommandParser)

    # Check if the description is set correctly
    assert parser.description == command.help

    # Check version argument
    version_action = [action for action in parser._actions if action.dest == 'version']
    assert len(version_action) == 1
    assert version_action[0].version == command.get_version()

    # Check verbosity argument
    verbosity_action = [action for action in parser._actions if action.dest == 'verbosity']
    assert verbosity_action
    assert verbosity_action[0].default == 1
    assert verbosity_action[0].choices == [0, 1, 2, 3]

    # Check settings argument
    settings_action = [action for action in parser._actions if action.dest == 'settings']
    assert settings_action

    # Check pythonpath argument
    pythonpath_action = [action for action in parser._actions if action.dest == 'pythonpath']
    assert pythonpath_action

    # Check traceback argument
    traceback_action = [action for action in parser._actions if action.dest == 'traceback']
    assert traceback_action

    # Check no-color argument
    no_color_action = [action for action in parser._actions if action.dest == 'no_color']
    assert no_color_action

    # Check force-color argument
    force_color_action = [action for action in parser._actions if action.dest == 'force_color']
    assert force_color_action

    # Check custom argument
    custom_arg_action = [action for action in parser._actions if action.dest == 'custom_arg']
    assert custom_arg_action