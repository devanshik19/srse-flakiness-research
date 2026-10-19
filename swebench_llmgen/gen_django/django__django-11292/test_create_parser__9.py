import pytest
import os
from argparse import ArgumentParser
from django.core.management.base import BaseCommand

class TestBaseCommand(BaseCommand):
    help = "Test Command"

    def get_version(self):
        return "1.0.0"

    def add_arguments(self, parser):
        parser.add_argument('--test', action='store_true', help='A test argument.')

def test_create_parser():
    command = TestBaseCommand(stdout=None, stderr=None, no_color=False, force_color=False)
    prog_name = "test_prog"
    subcommand = "test_subcommand"

    parser = command.create_parser(prog_name, subcommand)

    # Check parser prog
    assert parser.prog == "%s %s" % (os.path.basename(prog_name), subcommand)

    # Check arguments
    assert parser._optionals.choices[0].dest == 'version'
    assert parser._optionals.choices[1].dest == 'verbosity'
    assert parser._optionals.choices[2].dest == 'settings'
    assert parser._optionals.choices[3].dest == 'pythonpath'
    assert parser._optionals.choices[4].dest == 'traceback'
    assert parser._optionals.choices[5].dest == 'no_color'
    assert parser._optionals.choices[6].dest == 'force_color'
    assert parser._optionals.choices[7].dest == 'test'

    # Check default values
    assert parser.get_default('verbosity') == 1
    assert parser.get_default('test') is None

    # Check help and description
    assert parser.description == command.help