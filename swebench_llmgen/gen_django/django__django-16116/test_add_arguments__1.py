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

    # Test that the required arguments are added correctly
    args = parser.parse_args(['app_label'])
    assert args.args == ['app_label']

    # Test optional arguments
    optional_args = {
        '--dry-run': False,
        '--merge': False,
        '--empty': False,
        '--noinput': True,
        '-n': None,
        '--no-header': True,
        '--check': False,
        '--scriptable': False,
        '--update': False,
    }

    for arg, default in optional_args.items():
        if arg.startswith('--'):
            assert getattr(args, arg[2:], default) == default
        else:
            assert getattr(args, arg, default) == default

    # Test that a custom name can be supplied
    custom_args = parser.parse_args(['app_label', '--name', 'custom_name'])
    assert custom_args.name == 'custom_name'