import pytest
from django.core.management import CommandError
from django.core.management.commands.makemigrations import Command


@pytest.fixture
def command():
    return Command()


def test_add_arguments(command):
    parser = command.create_parser('manage.py', 'makemigrations')
    
    # Parse args for app_label (Position argument)
    args = ['app_label_1']
    namespace = parser.parse_args(args)
    assert namespace.args == ['app_label_1']

    # Test dry run argument
    args = ['app_label_1', '--dry-run']
    namespace = parser.parse_args(args)
    assert namespace.dry_run is True

    # Test merge argument
    args = ['app_label_1', '--merge']
    namespace = parser.parse_args(args)
    assert namespace.merge is True

    # Test empty argument
    args = ['app_label_1', '--empty']
    namespace = parser.parse_args(args)
    assert namespace.empty is True

    # Test noinput argument
    args = ['app_label_1', '--noinput']
    namespace = parser.parse_args(args)
    assert namespace.interactive is False

    # Test name argument
    args = ['app_label_1', '--name', 'custom_migration']
    namespace = parser.parse_args(args)
    assert namespace.name == 'custom_migration'

    # Test no-header argument
    args = ['app_label_1', '--no-header']
    namespace = parser.parse_args(args)
    assert namespace.include_header is False

    # Test check argument
    args = ['app_label_1', '--check']
    namespace = parser.parse_args(args)
    assert namespace.check_changes is True

    # Test scriptable argument
    args = ['app_label_1', '--scriptable']
    namespace = parser.parse_args(args)
    assert namespace.scriptable is True

    # Test update argument
    args = ['app_label_1', '--update']
    namespace = parser.parse_args(args)
    assert namespace.update is True