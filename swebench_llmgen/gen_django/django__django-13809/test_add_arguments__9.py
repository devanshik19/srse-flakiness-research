import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command

@pytest.fixture
def command():
    return Command()

def test_add_arguments(command):
    parser = command.create_parser('manage.py', 'runserver')
    command.add_arguments(parser)

    # Check that the positional argument 'addrport' is added
    assert 'addrport' in parser._actions[0].option_strings
    assert parser._actions[0].nargs == '?'

    # Check that the IPv6 option is added
    ipv6_action = next(action for action in parser._actions if '--ipv6' in action.option_strings)
    assert ipv6_action.dest == 'use_ipv6'
    assert ipv6_action.action == 'store_true'

    # Check that the nothreading option is added
    nothreading_action = next(action for action in parser._actions if '--nothreading' in action.option_strings)
    assert nothreading_action.dest == 'use_threading'
    assert nothreading_action.action == 'store_false'

    # Check that the noreload option is added
    noreload_action = next(action for action in parser._actions if '--noreload' in action.option_strings)
    assert noreload_action.dest == 'use_reloader'
    assert noreload_action.action == 'store_false'