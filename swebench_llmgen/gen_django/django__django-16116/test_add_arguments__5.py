import pytest
from django.core.management import CommandError
from django.core.management.commands.makemigrations import Command


def test_add_arguments():
    command = Command()
    parser = command.create_parser('test', 'makemigrations')

    # Simulate argument parsing
    args = ['app_label', '--dry-run', '--merge', '--empty', '--noinput', '--name', 'migration_name', '--no-header', '--check', '--scriptable', '--update']
    options = parser.parse_args(args)
    
    assert options.args == ['app_label']
    assert options.dry_run is True
    assert options.merge is True
    assert options.empty is True
    assert options.interactive is False
    assert options.name == 'migration_name'
    assert options.include_header is True
    assert options.check_changes is True
    assert options.scriptable is True
    assert options.update is True