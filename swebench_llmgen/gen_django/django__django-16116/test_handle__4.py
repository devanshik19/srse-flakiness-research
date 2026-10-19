import pytest
from django.core.management import CommandError
from django.contrib.auth.models import User
from django.apps import apps

@pytest.mark.parametrize(
    "app_labels, options, expected_migration_name, expected_exit_code",
    [
        (["auth"], {"verbosity": 1, "interactive": False, "dry_run": False,
                     "merge": False, "empty": False, "name": None,
                     "include_header": False, "check_changes": False, 
                     "scriptable": False, "update": False}, None, 0),
        (["auth"], {"verbosity": 1, "interactive": False, "dry_run": False,
                     "merge": False, "empty": False, "name": "valid_migration_name",
                     "include_header": False, "check_changes": False,
                     "scriptable": False, "update": False}, "valid_migration_name", 0),
        (["invalid_app"], {"verbosity": 1, "interactive": False, "dry_run": False,
                           "merge": False, "empty": False, "name": None,
                           "include_header": False, "check_changes": False,
                           "scriptable": False, "update": False}, None, 2),
        (["auth"], {"verbosity": 1, "interactive": False, "dry_run": False,
                     "merge": False, "empty": True, "name": None,
                     "include_header": False, "check_changes": False,
                     "scriptable": False, "update": False}, None, 0),
        ([], {"verbosity": 1, "interactive": False, "dry_run": False,
               "merge": False, "empty": True, "name": None,
               "include_header": False, "check_changes": False,
               "scriptable": False, "update": False}, None, CommandError),
    ]
)
def test_handle(app_labels, options, expected_migration_name, expected_exit_code):
    command = Command()
    if expected_exit_code == CommandError:
        with pytest.raises(CommandError):
            command.handle(*app_labels, **options)
    else:
        command.handle(*app_labels, **options)
        if options["empty"]:
            assert command.written_files  # Check that files were written for empty migration.
        # Additional validation can be added based on functionality.