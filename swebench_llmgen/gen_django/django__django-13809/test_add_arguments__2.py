import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command

@pytest.fixture
def command():
    return Command()

def test_add_arguments(command):
    parser = command.create_parser('manage.py', 'runserver')
    args = parser.parse_args(['runserver', '127.0.0.1:8000'])

    # Test default values
    assert args.addrport == '127.0.0.1:8000'
    assert args.use_ipv6 is False
    assert args.use_threading is True
    assert args.use_reloader is True

    # Test various flags
    args = parser.parse_args(['runserver', '127.0.0.1:8000', '--ipv6'])
    assert args.use_ipv6 is True

    args = parser.parse_args(['runserver', '127.0.0.1:8000', '--nothreading'])
    assert args.use_threading is False

    args = parser.parse_args(['runserver', '127.0.0.1:8000', '--noreload'])
    assert args.use_reloader is False

    args = parser.parse_args(['runserver', '127.0.0.1:8000', '--ipv6', '--nothreading', '--noreload'])
    assert args.use_ipv6 is True
    assert args.use_threading is False
    assert args.use_reloader is False