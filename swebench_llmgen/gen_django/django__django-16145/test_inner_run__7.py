import errno
import os
import socket
import sys
from datetime import datetime
from django.conf import settings
from django.core.management import CommandError
from django.core.management.commands.runserver import Command
from django.contrib.auth.models import User
import pytest

def test_inner_run_skip_checks(mocker):
    # Mock the required components
    command = Command()
    command.stdout = mocker.MagicMock()
    command.stderr = mocker.MagicMock()
    command.get_handler = mocker.Mock(return_value=lambda *args: None)
    command.check = mocker.MagicMock()
    command.check_migrations = mocker.MagicMock()
    command.get_version = mocker.Mock(return_value="4.0.0")
    command.addr = '127.0.0.1'
    command.port = '8000'
    command.protocol = 'http'
    command.use_ipv6 = False

    options = {
        "use_threading": False,
        "skip_checks": True,
        "shutdown_message": ""
    }
    
    # Call the inner_run method
    command.inner_run(args=[], options=options)

    # Assertions
    command.check_migrations.assert_called_once()
    command.stdout.write.assert_any_call(datetime.now().strftime("%B %d, %Y - %X"))
    command.stdout.write.assert_any_call(
        "Django version %(version)s, using settings %(settings)r\n"
        "Starting development server at %(protocol)s://%(addr)s:%(port)s/\n"
        "Quit the server with %(quit_command)s." % {
            "version": command.get_version(),
            "settings": settings.SETTINGS_MODULE,
            "protocol": command.protocol,
            "addr": command.addr,
            "port": command.port,
            "quit_command": 'CONTROL-C'
        }
    )

def test_inner_run_with_checks(mocker):
    command = Command()
    command.stdout = mocker.MagicMock()
    command.stderr = mocker.MagicMock()
    command.get_handler = mocker.Mock(return_value=lambda *args: None)
    command.check = mocker.MagicMock()
    command.check_migrations = mocker.MagicMock()
    command.get_version = mocker.Mock(return_value="4.0.0")
    command.addr = '127.0.0.1'
    command.port = '8000'
    command.protocol = 'http'
    command.use_ipv6 = False

    options = {
        "use_threading": False,
        "skip_checks": False,
        "shutdown_message": ""
    }
    
    command.inner_run(args=[], options=options)

    command.check.assert_called_once()
    command.check_migrations.assert_called_once()

def test_inner_run_address_in_use(mocker):
    command = Command()
    command.stdout = mocker.MagicMock()
    command.stderr = mocker.MagicMock()
    command.get_handler = mocker.Mock(return_value=lambda *args: None)
    command.check = mocker.MagicMock()
    command.check_migrations = mocker.MagicMock()
    command.get_version = mocker.Mock(return_value="4.0.0")
    command.addr = '127.0.0.1'
    command.port = '8000'
    command.protocol = 'http'
    command.use_ipv6 = False

    mocker.patch('django.core.servers.basehttp.run', side_effect=OSError(errno.EADDRINUSE, 'Port already in use'))

    options = {
        "use_threading": False,
        "skip_checks": False,
        "shutdown_message": ""
    }
    
    command.inner_run(args=[], options=options)

    command.stderr.write.assert_called_once_with("Error: That port is already in use.")

def test_inner_run_keyboard_interrupt(mocker):
    command = Command()
    command.stdout = mocker.MagicMock()
    command.stderr = mocker.MagicMock()
    command.get_handler = mocker.Mock(return_value=lambda *args: None)
    command.check = mocker.MagicMock()
    command.check_migrations = mocker.MagicMock()
    command.get_version = mocker.Mock(return_value="4.0.0")
    command.addr = '127.0.0.1'
    command.port = '8000'
    command.protocol = 'http'
    command.use_ipv6 = False

    mocker.patch('django.core.servers.basehttp.run', side_effect=KeyboardInterrupt)

    options = {
        "use_threading": False,
        "skip_checks": False,
        "shutdown_message": "Shutting down..."
    }
    
    with pytest.raises(SystemExit):
        command.inner_run(args=[], options=options)

    command.stdout.write.assert_called_once_with("Shutting down...")