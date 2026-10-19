import pytest
from django.core.management import CommandError
from django.apps import apps
from django.contrib.auth.models import User
from django.db import connections


@pytest.mark.parametrize("options, expected_exit_code", [
    ({"verbosity": 1, "interactive": False, "dry_run": False, "merge": False, "empty": False, "name": "test_migration", "include_header": False, "check_changes": False, "scriptable": False, "update": False}, 0),
    ({"verbosity": 1, "interactive": False, "dry_run": False, "merge": False, "empty": True, "name": "empty_migration", "include_header": False, "check_changes": False, "scriptable": False, "update": False}, 0),
    ({"verbosity": 1, "interactive": True, "dry_run": False, "merge": False, "empty": False, "name": None, "include_header": False, "check_changes": False, "scriptable": False, "update": False}, 1),
])
def test_command_handle(rf, options, expected_exit_code):
    command = Command()
    
    # Simulating command execution with valid app label
    command.handle('auth', **options)
    if expected_exit_code == 0:
        assert not command.written_files  # No migrations should be created when there are no changes
    else:
        with pytest.raises(SystemExit) as excinfo:
            command.handle('non_existing_app', **options)
        assert excinfo.value.code == 2  # Expecting an exit code of 2 for invalid app labels


def test_command_handle_conflicting_migrations(rf):
    command = Command()

    # Create conflicting migrations by setting up necessary User models and migrations
    # Let's assume there’s a migration conflict situation, testing the conflict handling
    # We can modify model attributes or similar for a mock situation

    command.merge = True  # Set merge option
    command.handle('auth')  # Call handle with 'auth' which should have conflicting migrations
    
    # Depending on the internal implementation, check if exception is raised correctly
    with pytest.raises(CommandError) as excinfo:
        command.handle('auth', merge=True)
    assert 'Conflicting migrations detected' in str(excinfo.value)