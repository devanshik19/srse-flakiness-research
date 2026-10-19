import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command

@pytest.fixture
def command():
    return Command()

def test_add_arguments(command):
    parser = command.create_parser('test', 'runserver')
    command.add_arguments(parser)

    # Check for default positionals
    args = parser.parse_args(['localhost:8000'])
    assert args.addrport == 'localhost:8000'

    # Check for the use_ipv6 flag
    args = parser.parse_args(['--ipv6', 'localhost:8000'])
    assert args.use_ipv6 is True

    # Check for the use_threading flag
    args = parser.parse_args(['--nothreading', 'localhost:8000'])
    assert args.use_threading is False

    # Check for the use_reloader flag
    args = parser.parse_args(['--noreload', 'localhost:8000'])
    assert args.use_reloader is False

    # Check that the addrport is still properly passed through
    args = parser.parse_args(['localhost:8000', '--noreload'])
    assert args.addrport == 'localhost:8000'
    assert args.use_reloader is False