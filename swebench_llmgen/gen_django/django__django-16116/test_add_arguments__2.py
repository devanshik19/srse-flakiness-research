import pytest
from django.core.management import CommandError
from django.core.management import Command
from unittest.mock import MagicMock

def test_add_arguments():
    command = Command()
    parser = MagicMock()
    
    command.add_arguments(parser)
    
    # Assert that the parser.add_argument method was called with the expected arguments
    assert parser.add_argument.call_count == 10
    
    expected_calls = [
        (("args",), {"metavar": "app_label", "nargs": "*", "help": "Specify the app label(s) to create migrations for."}),
        (("--dry-run",), {"action": "store_true", "help": "Just show what migrations would be made; don't actually write them."}),
        (("--merge",), {"action": "store_true", "help": "Enable fixing of migration conflicts."}),
        (("--empty",), {"action": "store_true", "help": "Create an empty migration."}),
        (("--noinput", "--no-input"), {"action": "store_false", "dest": "interactive", "help": "Tells Django to NOT prompt the user for input of any kind."}),
        (("-n", "--name"), {"help": "Use this name for migration file(s)."}),
        (("--no-header",), {"action": "store_false", "dest": "include_header", "help": "Do not add header comments to new migration file(s)."}),
        (("--check",), {"action": "store_true", "dest": "check_changes", "help": "Exit with a non-zero status if model changes are missing migrations."}),
        (("--scriptable",), {"action": "store_true", "dest": "scriptable", "help": "Divert log output and input prompts to stderr, writing only paths of generated migration files to stdout."}),
        (("--update",), {"action": "store_true", "dest": "update", "help": "Merge model changes into the latest migration and optimize the resulting operations."}),
    ]
    
    for index, (args, kwargs) in enumerate(expected_calls):
        parser.add_argument.assert_any_call(*args, **kwargs)