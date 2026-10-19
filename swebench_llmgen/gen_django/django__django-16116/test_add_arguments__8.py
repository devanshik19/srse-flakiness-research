import pytest
from django.core.management import CommandError
from django.core.management.commands.makemigrations import Command


@pytest.fixture
def parser():
    from argparse import ArgumentParser
    return ArgumentParser()


def test_add_arguments(parser):
    command = Command()
    command.add_arguments(parser)

    # Check that the app_label argument is added
    args = parser.parse_args(["app_label"])
    assert args.args == ["app_label"]

    # Check for the presence of optional arguments
    assert hasattr(args, 'dry_run')
    assert hasattr(args, 'merge')
    assert hasattr(args, 'empty')
    assert hasattr(args, 'interactive')
    assert hasattr(args, 'name')
    assert hasattr(args, 'include_header')
    assert hasattr(args, 'check_changes')
    assert hasattr(args, 'scriptable')
    assert hasattr(args, 'update')
    
    # Validate default values
    assert args.dry_run is False
    assert args.merge is False
    assert args.empty is False
    assert args.interactive is True
    assert args.include_header is True
    assert args.check_changes is False
    assert args.scriptable is False
    assert args.update is False