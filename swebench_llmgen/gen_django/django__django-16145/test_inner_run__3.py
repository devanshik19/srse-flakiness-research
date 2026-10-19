import errno
import os
import sys
import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command
from django.contrib.auth.models import User

def test_inner_run(mocker):
    command = Command()

    # Mock methods used in inner_run
    command.get_version = mocker.Mock(return_value="3.2")
    command.check = mocker.Mock()
    command.check_migrations = mocker.Mock()
    command.get_handler = mocker.Mock(return_value=lambda *args: None)
    command.stdout.write = mocker.Mock()
    command.stderr.write = mocker.Mock()

    # Set up options
    options = {
        "use_threading": True,
        "shutdown_message": "",
        "skip_checks": False,
        "addr": "127.0.0.1",
        "port": 8000,
        "protocol": "http",
        "use_ipv6": False,
        "server_cls": None,
    }
    
    # Test normal flow
    command.inner_run([], options)

    command.check.assert_called_once()
    command.check_migrations.assert_called_once()
    command.stdout.write.assert_any_call("Performing system checks...\n\n")
    command.stdout.write.assert_any_call("Django version 3.2, using settings 'None'\nStarting development server at http://127.0.0.1:8000/\nQuit the server with CONTROL-C.")

    # Test handling OSError
    mocker.patch('django.core.management.commands.runserver.run', side_effect=OSError(errno.EACCES, 'Permission denied'))
    command.stderr.write.reset_mock()

    with pytest.raises(SystemExit):  # Check for SystemExit to ensure exit on error
        command.inner_run([], options)
    
    command.stderr.write.assert_called_once_with("Error: You don't have permission to access that port.")

    # Test handling KeyboardInterrupt
    options["shutdown_message"] = "Server is shutting down."
    mocker.patch('django.core.management.commands.runserver.run', side_effect=KeyboardInterrupt)
    command.stdout.write.reset_mock()

    with pytest.raises(SystemExit):
        command.inner_run([], options)

    command.stdout.write.assert_called_once_with("Server is shutting down.")