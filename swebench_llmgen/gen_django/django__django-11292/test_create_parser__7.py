import pytest
import sys
from django.core.management.base import BaseCommand
from django.core.management import CommandParser

class TestBaseCommand(BaseCommand):

    def add_arguments(self, parser):
        # Sample implementation of base command add_arguments
        parser.add_argument('--sample', help='Sample argument for testing.')

    def get_version(self):
        return "1.0.0"

def test_create_parser_version():
    command = TestBaseCommand(stdout=sys.stdout, stderr=sys.stderr, no_color=False, force_color=False)
    parser = command.create_parser(prog_name='testprog', subcommand='testsubcommand')

    assert isinstance(parser, CommandParser)
    assert '--version' in [action.dest for action in parser._actions]
    assert '--verbosity' in [action.dest for action in parser._actions]

def test_create_parser_settings():
    command = TestBaseCommand(stdout=sys.stdout, stderr=sys.stderr, no_color=False, force_color=False)
    parser = command.create_parser(prog_name='testprog', subcommand='testsubcommand')

    assert '--settings' in [action.dest for action in parser._actions]

def test_create_parser_pythonpath():
    command = TestBaseCommand(stdout=sys.stdout, stderr=sys.stderr, no_color=False, force_color=False)
    parser = command.create_parser(prog_name='testprog', subcommand='testsubcommand')

    assert '--pythonpath' in [action.dest for action in parser._actions]

def test_create_parser_traceback():
    command = TestBaseCommand(stdout=sys.stdout, stderr=sys.stderr, no_color=False, force_color=False)
    parser = command.create_parser(prog_name='testprog', subcommand='testsubcommand')

    assert '--traceback' in [action.dest for action in parser._actions]

def test_create_parser_color_options():
    command = TestBaseCommand(stdout=sys.stdout, stderr=sys.stderr, no_color=False, force_color=False)
    parser = command.create_parser(prog_name='testprog', subcommand='testsubcommand')

    assert '--no-color' in [action.dest for action in parser._actions]
    assert '--force-color' in [action.dest for action in parser._actions]