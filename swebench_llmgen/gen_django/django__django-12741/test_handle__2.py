import pytest
from django.core.management import CommandError
from django.contrib.auth.models import User
from django.db import connections

@pytest.mark.parametrize("interactive, expected_output, flush_confirm", [
    (True, "You have requested a flush of the database.\n", "yes"),
    (False, None, "yes"),
])
def test_handle_flush(interactive, expected_output, flush_confirm, monkeypatch):
    # Prepare the options for the command
    options = {
        'database': 'default',
        'verbosity': 1,
        'interactive': interactive,
        'reset_sequences': True,
        'allow_cascade': False,
        'inhibit_post_migrate': False,
    }
    
    # Create a user to have a table in the database
    User.objects.create_user(username='testuser', password='testpass')

    command = Command()
    
    # Simulate user input for the interactive mode
    if interactive:
        monkeypatch.setattr('builtins.input', lambda _: flush_confirm)
    
    # Capture stdout to verify the output messages
    from django.core.management.base import CommandError
    from django.core.management import call_command
    
    if expected_output:
        with pytest.raises(CommandError) as exc_info:
            command.handle(**options)
        assert "Flush cancelled." in str(exc_info.value)
    else:
        command.handle(**options)
        
        # Ensure the User table is empty after flush
        assert User.objects.count() == 0
        
        # Ensure that the command does not raise an error
        try:
            command.handle(**options)
        except CommandError:
            pytest.fail("Command raised CommandError unexpectedly!")