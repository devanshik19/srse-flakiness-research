import pytest
from django.core.management.base import BaseCommand
from django.core.management import CommandParser

class TestBaseCommand(BaseCommand):
    help = "Test help message"

    def add_arguments(self, parser):
        parser.add_argument('--test-arg', help='A test argument.')

    def get_version(self):
        return '1.0.0'

def test_create_parser():
    command = TestBaseCommand(stdout=None, stderr=None, no_color=False, force_color=False)
    prog_name = "test_prog"
    subcommand = "test_subcommand"
    
    parser = command.create_parser(prog_name, subcommand)
    
    assert isinstance(parser, CommandParser)
    assert parser.prog == "test_prog test_subcommand"
    assert parser.description == "Test help message"
        
    # Check the --version argument
    version_action = [action for action in parser._actions if action.dest == 'version'][0]
    assert version_action.version == '1.0.0'
    
    # Check verbosity argument
    verbosity_action = [action for action in parser._actions if action.dest == 'verbosity'][0]
    assert verbosity_action.choices == [0, 1, 2, 3]
    assert verbosity_action.default == 1
    
    # Check settings argument
    settings_action = [action for action in parser._actions if action.dest == 'settings'][0]
    assert settings_action.help.startswith('The Python path to a settings module')
    
    # Check pythonpath argument
    pythonpath_action = [action for action in parser._actions if action.dest == 'pythonpath'][0]
    assert pythonpath_action.help == 'A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".'

    # Check traceback argument
    traceback_action = [action for action in parser._actions if action.dest == 'traceback'][0]
    assert traceback_action.help == 'Raise on CommandError exceptions'
    
    # Check no-color argument
    no_color_action = [action for action in parser._actions if action.dest == 'no_color'][0]
    assert no_color_action.help == "Don't colorize the command output."
    
    # Check force-color argument
    force_color_action = [action for action in parser._actions if action.dest == 'force_color'][0]
    assert force_color_action.help == 'Force colorization of the command output.'
    
    # Check test-arg
    test_arg_action = [action for action in parser._actions if action.dest == 'test_arg'][0]
    assert test_arg_action.help == 'A test argument.'