import pytest
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand

@pytest.fixture
def command():
    return MakemigrationsCommand()

def test_add_arguments(command):
    parser = BaseCommand.create_parser('makemigrations', 'test')

    command.add_arguments(parser)
    
    # Simulate command line parsing
    args = ['app_label', '--dry-run', '--merge', '--empty', 
            '--noinput', '--name', 'migration_name', 
            '--no-header', '--check', '--scriptable', '--update']
    
    namespace = parser.parse_args(args)
    
    assert namespace.args == ['app_label']
    assert namespace.dry_run is True
    assert namespace.merge is True
    assert namespace.empty is True
    assert namespace.interactive is False
    assert namespace.name == 'migration_name'
    assert namespace.include_header is False
    assert namespace.check_changes is True
    assert namespace.scriptable is True
    assert namespace.update is True

    # Check default values for unspecified args
    default_args = parser.parse_args(['app_label'])
    assert default_args.dry_run is False
    assert default_args.merge is False
    assert default_args.empty is False
    assert default_args.interactive is True
    assert default_args.name is None
    assert default_args.include_header is True
    assert default_args.check_changes is False
    assert default_args.scriptable is False
    assert default_args.update is False