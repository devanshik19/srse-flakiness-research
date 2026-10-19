import pytest
import sys
from django.core.management.base import BaseCommand

class TestBaseCommand(BaseCommand):
    
    def create_parser(self, prog_name, subcommand, **kwargs):
        parser = super().create_parser(prog_name, subcommand, **kwargs)
        return parser

    def test_create_parser_with_default_values(self):
        command = TestBaseCommand(stdout=sys.stdout, stderr=sys.stderr, no_color=False, force_color=False)
        parser = command.create_parser('manage.py', 'testcommand')

        assert parser.prog == 'manage.py testcommand'
        assert '--version' in [arg.dest for arg in parser._actions]
        assert parser.get_default('verbosity') == 1
        assert parser.get_default('no_color') is False
        assert parser.get_default('force_color') is False

    def test_create_parser_with_custom_args(self):
        command = TestBaseCommand(stdout=sys.stdout, stderr=sys.stderr, no_color=False, force_color=False)
        parser = command.create_parser('manage.py', 'testcommand', custom_arg='value')

        assert 'custom_arg' in [arg.dest for arg in parser._actions]

    def test_create_parser_with_help(self):
        command = TestBaseCommand(stdout=sys.stdout, stderr=sys.stderr, no_color=False, force_color=False)
        command.help = "Test command help"
        parser = command.create_parser('manage.py', 'testcommand')

        assert parser.description == "Test command help"

    def test_create_parser_with_env_var_settings(self):
        command = TestBaseCommand(stdout=sys.stdout, stderr=sys.stderr, no_color=False, force_color=False)
        parser = command.create_parser('manage.py', 'testcommand')

        assert '--settings' in [arg.dest for arg in parser._actions]