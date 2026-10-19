import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command as RunserverCommand
from django.contrib.auth.models import User
import socket
import threading


def test_inner_run_success(mocker):
    mock_check_migrations = mocker.patch.object(RunserverCommand, 'check_migrations')
    mock_get_handler = mocker.patch.object(RunserverCommand, 'get_handler', return_value=lambda x, y: None)
    mock_run = mocker.patch('django.core.servers.basehttp.run')

    command = RunserverCommand()
    command.stdout = mocker.Mock()
    command.stderr = mocker.Mock()
    command.protocol = 'http'
    command.addr = '127.0.0.1'
    command.port = 8000
    command.use_ipv6 = False

    options = {
        'use_threading': True,
        'shutdown_message': '',
    }

    command.inner_run([], options)

    mock_check_migrations.assert_called_once()
    mock_get_handler.assert_called_once()
    mock_run.assert_called_once_with('127.0.0.1', 8000, mock_get_handler.return_value, ipv6=False, threading=True,
                                      server_cls=command.server_cls)


def test_inner_run_oserror_permission_denied(mocker):
    mock_check_migrations = mocker.patch.object(RunserverCommand, 'check_migrations')
    mock_get_handler = mocker.patch.object(RunserverCommand, 'get_handler', return_value=lambda x, y: None)
    mock_run = mocker.patch('django.core.servers.basehttp.run', side_effect=OSError(errno.EACCES, 'Permission denied'))

    command = RunserverCommand()
    command.stderr = mocker.Mock()

    options = {
        'use_threading': True,
        'shutdown_message': '',
    }

    command.inner_run([], options)

    command.stderr.write.assert_called_once_with("Error: You don't have permission to access that port.")
    

def test_inner_run_oserror_address_in_use(mocker):
    mock_check_migrations = mocker.patch.object(RunserverCommand, 'check_migrations')
    mock_get_handler = mocker.patch.object(RunserverCommand, 'get_handler', return_value=lambda x, y: None)
    mock_run = mocker.patch('django.core.servers.basehttp.run', side_effect=OSError(errno.EADDRINUSE, 'Address in use'))

    command = RunserverCommand()
    command.stderr = mocker.Mock()

    options = {
        'use_threading': True,
        'shutdown_message': '',
    }

    command.inner_run([], options)

    command.stderr.write.assert_called_once_with("Error: That port is already in use.")


def test_inner_run_oserror_address_not_available(mocker):
    mock_check_migrations = mocker.patch.object(RunserverCommand, 'check_migrations')
    mock_get_handler = mocker.patch.object(RunserverCommand, 'get_handler', return_value=lambda x, y: None)
    mock_run = mocker.patch('django.core.servers.basehttp.run', side_effect=OSError(errno.EADDRNOTAVAIL, 'Address not available'))

    command = RunserverCommand()
    command.stderr = mocker.Mock()

    options = {
        'use_threading': True,
        'shutdown_message': '',
    }

    command.inner_run([], options)

    command.stderr.write.assert_called_once_with("Error: That IP address can't be assigned to.")


def test_inner_run_keyboard_interrupt(mocker):
    command = RunserverCommand()
    command.stdout = mocker.Mock()

    options = {
        'use_threading': True,
        'shutdown_message': 'Shutting down...',
    }
    
    mocker.patch.object(command, 'get_handler', return_value=lambda x, y: None)
    mocker.patch('django.core.servers.basehttp.run', side_effect=KeyboardInterrupt)

    with pytest.raises(SystemExit):
        command.inner_run([], options)

    command.stdout.write.assert_called_once_with('Shutting down...')