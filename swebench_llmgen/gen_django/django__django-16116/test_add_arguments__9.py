import pytest
from django.core.management import CommandError
from django.core.management.commands.makemigrations import Command

def test_add_arguments():
    command = Command()
    parser = command.create_parser('manage.py', 'makemigrations')

    # Check that all arguments are added correctly
    args = parser._actions

    # Test positional argument
    assert any(arg.dest == 'args' for arg in args)
    assert any(arg.metavar == 'app_label' for arg in args)

    # Test optional arguments
    assert any(arg.dest == 'dry_run' for arg in args)
    assert any(arg.dest == 'merge' for arg in args)
    assert any(arg.dest == 'empty' for arg in args)
    assert any(arg.dest == 'interactive' for arg in args)
    assert any(arg.dest == 'name' for arg in args)
    assert any(arg.dest == 'include_header' for arg in args)
    assert any(arg.dest == 'check_changes' for arg in args)
    assert any(arg.dest == 'scriptable' for arg in args)
    assert any(arg.dest == 'update' for arg in args)

    # Verify flag types
    dry_run_action = next(arg for arg in args if arg.dest == 'dry_run')
    assert dry_run_action.action == 'store_true'

    merge_action = next(arg for arg in args if arg.dest == 'merge')
    assert merge_action.action == 'store_true'

    empty_action = next(arg for arg in args if arg.dest == 'empty')
    assert empty_action.action == 'store_true'

    no_input_action = next(arg for arg in args if arg.dest == 'interactive')
    assert no_input_action.dest == 'interactive'
    assert no_input_action.action == 'store_false'

    # Check help text assertions
    assert "Specify the app label(s) to create migrations for." in next(arg for arg in args if arg.dest == 'args').help
    assert "Just show what migrations would be made; don't actually write them." in dry_run_action.help
    assert "Enable fixing of migration conflicts." in merge_action.help
    assert "Create an empty migration." in empty_action.help
    assert "Tells Django to NOT prompt the user for input of any kind." in no_input_action.help
    assert "Use this name for migration file(s)." in next(arg for arg in args if arg.dest == 'name').help
    assert "Do not add header comments to new migration file(s)." in next(arg for arg in args if arg.dest == 'include_header').help
    assert "Exit with a non-zero status if model changes are missing migrations." in next(arg for arg in args if arg.dest == 'check_changes').help
    assert "Divert log output and input prompts to stderr, writing only paths of generated migration files to stdout." in next(arg for arg in args if arg.dest == 'scriptable').help
    assert "Merge model changes into the latest migration and optimize the resulting operations." in next(arg for arg in args if arg.dest == 'update').help