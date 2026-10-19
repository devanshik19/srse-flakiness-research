import errno
import os
import sys
import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command
from django.contrib.auth.models import User

def test_inner_run_system_checks(mocker):
    command = Command()
    mocker.patch.object(command, 'check')
    mocker.patch.object(command, 'check_migrations')
    mocker.patch.object(command, 'get_handler', return_value=None)
    mocker.patch('django.core.servers.basehttp.run')

    options = {
        'use_threading': False,
        'skip_checks': False,
        'shutdown_message': '',
        'port': '8000',
        'addr': '127.0.0.1',
        'protocol': 'http',
    }
    
    command.stdout.write = mocker.Mock()
    command.stderr.write = mocker.Mock()

    command.inner_run([], options)

    command.check.assert_called_once()
    command.check_migrations.assert_called_once()
    assert command.stdout.write.call_count == 3  # for system checks, date, and server start message

def test_inner_run_port_access_error(mocker):
    command = Command()
    mocker.patch('django.core.servers.basehttp.run', side_effect=OSError(errno.EACCES, "Permission denied"))
    
    options = {
        'use_threading': False,
        'skip_checks': False,
        'shutdown_message': '',
        'port': '8000',
        'addr': '127.0.0.1',
        'protocol': 'http',
    }

    command.stderr.write = mocker.Mock()

    with pytest.raises(SystemExit):
        command.inner_run([], options)

    command.stderr.write.assert_called_once_with("Error: You don't have permission to access that port.")
    
def test_inner_run_keyboard_interrupt(mocker):
    command = Command()
    mocker.patch.object(command, 'get_handler', return_value=None)
    mocker.patch('django.core.servers.basehttp.run', side_effect=KeyboardInterrupt)
    
    options = {
        'use_threading': False,
        'skip_checks': False,
        'shutdown_message': 'Server is shutting down...',
        'port': '8000',
        'addr': '127.0.0.1',
        'protocol': 'http',
    }

    command.stdout.write = mocker.Mock()

    with pytest.raises(SystemExit):
        command.inner_run([], options)

    command.stdout.write.assert_called_once_with('Server is shutting down...')