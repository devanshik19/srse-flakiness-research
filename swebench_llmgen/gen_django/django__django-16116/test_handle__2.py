import pytest
from django.core.management import CommandError
from django.contrib.auth.models import User
from django.apps import apps

@pytest.mark.parametrize("options, expected_exit_code", [
    ({"verbosity": 1, "interactive": False, "dry_run": False, "merge": False, 
      "empty": False, "name": "valid_migration_name", "include_header": False, 
      "check_changes": False, "scriptable": False, "update": False}, 0),
    ({"verbosity": 1, "interactive": False, "dry_run": False, "merge": False, 
      "empty": True, "name": "valid_migration_name", "include_header": False, 
      "check_changes": False, "scriptable": False, "update": False}, 0),
    ({"verbosity": 1, "interactive": False, "dry_run": False, "merge": False, 
      "empty": False, "name": "invalid migration name", "include_header": False, 
      "check_changes": False, "scriptable": False, "update": False}, 2),
])
def test_handle(options, expected_exit_code):
    command = Command()
    
    # Create a valid app label for testing
    if not apps.is_installed('auth'):
        raise RuntimeError("Auth app is not installed.")
    
    app_label = "auth"

    # Call handle method and catch CommandError for invalid names
    if "name" in options and not options["name"].isidentifier():
        with pytest.raises(CommandError, match="The migration name must be a valid Python identifier."):
            command.handle(app_label, **options)
    else:
        if options.get("empty"):
            command.handle(app_label, **options)
            assert command.written_files  # Ensure files are written for empty migration
        
        command.handle(app_label, **options)
        assert command.written_files  # Ensure files are written if there are changes