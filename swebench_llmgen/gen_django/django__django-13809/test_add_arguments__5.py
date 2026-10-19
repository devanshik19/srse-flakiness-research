import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command

@pytest.fixture
def command():
    return Command()

def test_add_arguments(command):
    parser = command.create_parser('test', 'runserver')
    command.add_arguments(parser)
    
    # Check if 'addrport' argument is added
    args = parser.parse_args(['test'])
    assert args.addrport == 'test'

    # Check if '--ipv6' flag is added and works
    args = parser.parse_args(['test', '--ipv6'])
    assert args.use_ipv6 is True

    # Check if '--nothreading' flag is added and works
    args = parser.parse_args(['test', '--nothreading'])
    assert args.use_threading is False

    # Check if '--noreload' flag is added and works
    args = parser.parse_args(['test', '--noreload'])
    assert args.use_reloader is False

    # Check that no arguments defaults work correctly
    args = parser.parse_args([])
    assert args.addrport is None
    assert args.use_ipv6 is False
    assert args.use_threading is True
    assert args.use_reloader is True