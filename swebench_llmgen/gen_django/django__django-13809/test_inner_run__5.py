import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command
from unittest.mock import patch, MagicMock
import socket

def test_inner_run_success():
    command = Command()
    command.stdout = MagicMock()
    command.stderr = MagicMock()
    command.get_handler = MagicMock(return_value=MagicMock())
    command.check = MagicMock()
    command.check_migrations = MagicMock()
    command.get_version = MagicMock(return_value="4.0")
    command.addr = "127.0.0.1"
    command.port = 8000
    command.use_ipv6 = False
    command.protocol = "http"

    options = {
        'use_threading': True,
        'shutdown_message': '',
    }
    
    with patch('django.core.servers.basehttp.run') as mock_run:
        command.inner_run([], options)
        
        command.check.assert_called_once()
        command.check_migrations.assert_called_once()
        command.get_handler.assert_called_once_with([], options)
        mock_run.assert_called_once_with(
            command.addr,
            int(command.port),
            command.get_handler(),
            ipv6=command.use_ipv6,
            threading=options['use_threading'],
            server_cls=command.server_cls,
        )

def test_inner_run_os_error():
    command = Command()
    command.stdout = MagicMock()
    command.stderr = MagicMock()
    command.get_handler = MagicMock(return_value=MagicMock())
    command.check = MagicMock()
    command.check_migrations = MagicMock()
    command.get_version = MagicMock(return_value="4.0")
    command.addr = "127.0.0.1"
    command.port = 8000
    command.use_ipv6 = False
    command.protocol = "http"
    
    options = {
        'use_threading': True,
        'shutdown_message': '',
    }

    with patch('django.core.servers.basehttp.run', side_effect=OSError(errno.EACCES, "Permission denied")):
        command.inner_run([], options)
        command.stderr.write.assert_called_once_with("Error: You don't have permission to access that port.")
        
def test_inner_run_keyboard_interrupt():
    command = Command()
    command.stdout = MagicMock()
    command.stderr = MagicMock()
    command.get_handler = MagicMock(return_value=MagicMock())
    command.check = MagicMock()
    command.check_migrations = MagicMock()
    command.get_version = MagicMock(return_value="4.0")
    command.addr = "127.0.0.1"
    command.port = 8000
    command.use_ipv6 = False
    command.protocol = "http"
    
    options = {
        'use_threading': True,
        'shutdown_message': 'Shutting down...',
    }

    with patch('django.core.servers.basehttp.run', side_effect=KeyboardInterrupt):
        with pytest.raises(SystemExit):
            command.inner_run([], options)
        command.stdout.write.assert_called_once_with('Shutting down...')