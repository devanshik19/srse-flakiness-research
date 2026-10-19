import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command

@pytest.fixture
def command():
    return Command()

def test_add_arguments_without_addrport(command):
    parser = command.create_argparse()
    assert 'addrport' in parser._actions[0].dest
    assert parser._actions[0].nargs == '?'

def test_add_arguments_with_ipv6(command):
    parser = command.create_argparse()
    assert '--ipv6' in [action.option_strings[0] for action in parser._actions]
    assert parser._actions[-3].dest == 'use_ipv6'

def test_add_arguments_with_nothreading(command):
    parser = command.create_argparse()
    assert '--nothreading' in [action.option_strings[0] for action in parser._actions]
    assert parser._actions[-2].dest == 'use_threading'

def test_add_arguments_with_noreload(command):
    parser = command.create_argparse()
    assert '--noreload' in [action.option_strings[0] for action in parser._actions]
    assert parser._actions[-1].dest == 'use_reloader'