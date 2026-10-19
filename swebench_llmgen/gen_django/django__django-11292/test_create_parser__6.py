import os
import pytest
from django.core.management.base import BaseCommand

class TestBaseCommand(BaseCommand):
    def __init__(self):
        self.help = "Test command help"
        self._called_from_command_line = True
    
    def get_version(self):
        return "1.0.0"
    
    def add_arguments(self, parser):
        parser.add_argument('--test-arg', help='A test argument')

@pytest.fixture
def command_instance():
    return TestBaseCommand()

def test_create_parser(command_instance):
    prog_name = 'manage.py'
    subcommand = 'test_command'
    
    parser = command_instance.create_parser(prog_name, subcommand)
    
    # Check parser attributes
    assert parser.prog == 'manage.py test_command'
    assert parser.description == "Test command help"
    
    # Check version argument
    version_action = parser._actions[0]
    assert version_action.dest == 'version'
    
    # Check verbosity argument
    verbosity_action = next(action for action in parser._actions if action.dest == 'verbosity')
    assert verbosity_action.choices == [0, 1, 2, 3]
    assert verbosity_action.default == 1
    
    # Check settings argument
    settings_action = next(action for action in parser._actions if action.dest == 'settings')
    assert settings_action.help == (
        'The Python path to a settings module, e.g. '
        '"myproject.settings.main". If this isn\'t provided, the '
        'DJANGO_SETTINGS_MODULE environment variable will be used.'
    )

    # Check additional test argument
    test_arg_action = next(action for action in parser._actions if action.dest == 'test_arg')
    assert test_arg_action.help == 'A test argument'
    
    # Check exception flags
    assert '--traceback' in [action.dest for action in parser._actions]
    assert '--no-color' in [action.dest for action in parser._actions]
    assert '--force-color' in [action.dest for action in parser._actions]