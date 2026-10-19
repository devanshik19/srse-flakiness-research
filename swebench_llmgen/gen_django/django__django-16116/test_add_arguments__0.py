import pytest
from django.core.management import CommandError
from django.core.management.commands.makemigrations import Command

@pytest.fixture
def command():
    return Command()

def test_add_arguments(command):
    parser = command.create_parser('makemigrations', 'test_cmd')

    # Check if all arguments are added correctly
    args = [action.dest for action in parser._actions]

    expected_args = [
        'args',
        'dry_run',
        'merge',
        'empty',
        'interactive',
        'name',
        'include_header',
        'check_changes',
        'scriptable',
        'update'
    ]

    # Assert all expected arguments are there
    for expected_arg in expected_args:
        assert expected_arg in args

    # Test if each argument has the correct properties
    assert next((action for action in parser._actions if action.dest == 'dry_run')).option_strings == ['--dry-run']
    assert next((action for action in parser._actions if action.dest == 'merge')).option_strings == ['--merge']
    assert next((action for action in parser._actions if action.dest == 'empty')).option_strings == ['--empty']
    assert next((action for action in parser._actions if action.dest == 'interactive')).option_strings == ['--noinput', '--no-input']
    assert next((action for action in parser._actions if action.dest == 'name')).option_strings == ['-n', '--name']
    assert next((action for action in parser._actions if action.dest == 'include_header')).option_strings == ['--no-header']
    assert next((action for action in parser._actions if action.dest == 'check_changes')).option_strings == ['--check']
    assert next((action for action in parser._actions if action.dest == 'scriptable')).option_strings == ['--scriptable']
    assert next((action for action in parser._actions if action.dest == 'update')).option_strings == ['--update']