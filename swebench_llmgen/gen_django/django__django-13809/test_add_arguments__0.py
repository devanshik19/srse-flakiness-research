import pytest
from django.core.management import CommandParser
from django.core.management.commands.runserver import Command

@pytest.fixture
def command():
    return Command()

def test_add_arguments(command):
    parser = CommandParser()
    command.add_arguments(parser)

    # Check that positional argument 'addrport' is added
    assert 'addrport' in parser._actions[0].dest
    assert parser._actions[0].nargs == '?'
    assert parser._actions[0].help == 'Optional port number, or ipaddr:port'

    # Check that '--ipv6' argument is added
    assert '--ipv6' in [action.option_strings for action in parser._actions]
    assert parser._actions[1].dest == 'use_ipv6'
    assert parser._actions[1].action == 'store_true'
    assert parser._actions[1].help == 'Tells Django to use an IPv6 address.'

    # Check that '--nothreading' argument is added
    assert '--nothreading' in [action.option_strings for action in parser._actions]
    assert parser._actions[2].dest == 'use_threading'
    assert parser._actions[2].action == 'store_false'
    assert parser._actions[2].help == 'Tells Django to NOT use threading.'

    # Check that '--noreload' argument is added
    assert '--noreload' in [action.option_strings for action in parser._actions]
    assert parser._actions[3].dest == 'use_reloader'
    assert parser._actions[3].action == 'store_false'
    assert parser._actions[3].help == 'Tells Django to NOT use the auto-reloader.'