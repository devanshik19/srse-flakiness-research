import pytest
from django.core.management.base import BaseCommand
from django.core.management import CommandParser

class TestBaseCommand(BaseCommand):
    def create_parser(self, prog_name, subcommand, **kwargs):
        parser = CommandParser(
            prog='%s %s' % (os.path.basename(prog_name), subcommand),
            description=self.help or None,
            formatter_class=None,
            **kwargs
        )
        parser.add_argument('--version', action='version', version=self.get_version())
        parser.add_argument(
            '-v', '--verbosity', default=1,
            type=int, choices=[0, 1, 2, 3],
        )
        parser.add_argument('--settings', help='Python path to a settings module.')
        parser.add_argument('--pythonpath', help='A directory to add to the Python path.')
        parser.add_argument('--traceback', action='store_true', help='Raise on CommandError exceptions')
        parser.add_argument('--no-color', action='store_true', help="Don't colorize output.")
        parser.add_argument('--force-color', action='store_true', help='Force colorization of output.')
        return parser

def test_create_parser():
    command = TestBaseCommand()
    command.help = "Test command help"
    
    parser = command.create_parser('manage.py', 'testcommand')

    # Check main parameters
    assert parser.prog == 'manage.py testcommand'
    assert parser.description == "Test command help"

    # Check version argument
    version_arg = parser._actions[0]
    assert version_arg.option_strings == ['--version']

    # Check verbosity argument
    verbosity_arg = parser._actions[1]
    assert verbosity_arg.dest == 'verbosity'
    assert verbosity_arg.default == 1
    assert verbosity_arg.choices == [0, 1, 2, 3]

    # Check settings argument
    settings_arg = next(arg for arg in parser._actions if arg.dest == 'settings')
    assert settings_arg.help == 'Python path to a settings module.'

    # Check pythonpath argument
    pythonpath_arg = next(arg for arg in parser._actions if arg.dest == 'pythonpath')
    assert pythonpath_arg.help == 'A directory to add to the Python path.'

    # Check traceback argument
    traceback_arg = next(arg for arg in parser._actions if arg.dest == 'traceback')
    assert traceback_arg.action == 'store_true'

    # Check no-color argument
    no_color_arg = next(arg for arg in parser._actions if arg.dest == 'no_color')
    assert no_color_arg.action == 'store_true'

    # Check force-color argument
    force_color_arg = next(arg for arg in parser._actions if arg.dest == 'force_color')
    assert force_color_arg.action == 'store_true'