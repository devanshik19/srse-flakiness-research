import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.apps import apps
from django.contrib.auth.models import User

@pytest.mark.parametrize("verbosity, interactive, dry_run, merge, empty, migration_name, check_changes, expected_output", [
    (1, True, False, False, False, None, False, "No changes detected in app 'auth'"),
    (1, False, False, False, False, None, True, "No changes detected in app 'auth'"),
    (1, True, False, True, False, None, False, "No conflicts detected to merge."),
])
def test_handle_no_changes(verbosity, interactive, dry_run, merge, empty, migration_name, check_changes, expected_output):
    User.objects.create_user("testuser", "test@example.com", "password")  # Create a user to have a model
    options = {
        'verbosity': verbosity,
        'interactive': interactive,
        'dry_run': dry_run,
        'merge': merge,
        'empty': empty,
        'name': migration_name,
        'exit_code': False,
        'check_changes': check_changes,
    }
    
    if expected_output:
        with pytest.raises(SystemExit):
            call_command('makemigrations', 'auth', **options)
    else:
        call_command('makemigrations', 'auth', **options)

def test_handle_invalid_app_label():
    options = {
        'verbosity': 1,
        'interactive': False,
        'dry_run': False,
        'merge': False,
        'empty': False,
        'name': None,
        'exit_code': False,
        'check_changes': False,
    }
    with pytest.raises(SystemExit) as e:
        call_command('makemigrations', 'invalid_app', **options)
    assert e.value.code == 2

def test_handle_empty_migration():
    options = {
        'verbosity': 1,
        'interactive': False,
        'dry_run': False,
        'merge': False,
        'empty': True,
        'name': 'empty_migration',
        'exit_code': False,
        'check_changes': False,
    }
    call_command('makemigrations', 'auth', **options)  # Should create an empty migration without errors

def test_handle_merge_with_conflicts():
    # Create initial migrations for User model
    User.objects.create_user("testuser", "test@example.com", "password")
    
    # Mimic migration conflict by directly modifying a migration file or loader (requires setup in full example)
    
    options = {
        'verbosity': 1,
        'interactive': True,
        'dry_run': False,
        'merge': True,
        'empty': False,
        'name': None,
        'exit_code': False,
        'check_changes': False,
    }
    with pytest.raises(CommandError) as e:
        call_command('makemigrations', 'auth', **options)
    assert "Conflicting migrations detected" in str(e.value)