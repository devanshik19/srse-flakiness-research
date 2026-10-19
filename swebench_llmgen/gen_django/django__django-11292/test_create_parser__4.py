import os
import pytest
from django.core.management.base import BaseCommand
from django.core.management.parser import CommandParser


class TestBaseCommand(BaseCommand):
    help = 'Test command help text'

    def add_arguments(self, parser):
        parser.add_argument('--test-arg', type=str, help='A test argument')


def test_create_parser():
    command = TestBaseCommand(stdout=None, stderr=None, no_color=False, force_color=False)
    prog_name = 'manage.py'
    subcommand = 'test'

    parser = command.create_parser(prog_name, subcommand)

    # Check prog name and subcommand in parser
    assert parser.prog == f'{os.path.basename(prog_name)} {subcommand}'

    # Check help text
    assert parser.description == command.help

    # Check default arguments
    assert '--version' in parser._optionals._option_string_actions
    assert parser.get_default('verbosity') == 1
    assert parser.get_default('settings') is None
    assert parser.get_default('pythonpath') is None
    assert not parser.get_default('traceback')
    assert not parser.get_default('no_color')
    assert not parser.get_default('force_color')

    # Check custom arguments
    test_arg_action = parser._optionals._option_string_actions['--test-arg']
    assert test_arg_action.help == 'A test argument'
    assert test_arg_action.type == str