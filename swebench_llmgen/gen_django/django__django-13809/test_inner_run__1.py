import sys
import pytest
import threading
from django.core.management import CommandError
from django.core.management.commands.runserver import Command
from unittest.mock import patch, MagicMock

@pytest.fixture
def command():
    return Command()

def test_inner_run_success(command):
    command.stdout = MagicMock()
    command.stderr = MagicMock()
    command.get_handler = MagicMock(return_value='handler')
    command.check = MagicMock()
    command.check_migrations = MagicMock()
    command.port = 8000
    command.addr = '127.0.0.1'
    command.protocol = 'http'
    command.use_ipv6 = False

    with patch('django.core.servers.basehttp.run') as mock_run:
        command.inner_run(use_threading=True)

        command.check.assert_called()
        command.check_migrations.assert_called()
        command.stdout.write.assert_called()
        mock_run.assert_called_once_with(
            command.addr, 
            int(command.port), 
            'handler', 
            ipv6=False, 
            threading=True, 
            server_cls=command.server_cls
        )

def test_inner_run_os_error(command):
    command.stdout = MagicMock()
    command.stderr = MagicMock()
    command.get_handler = MagicMock(return_value='handler')
    command.check = MagicMock()
    command.check_migrations = MagicMock()
    command.port = 8000
    command.addr = '127.0.0.1'
    command.protocol = 'http'
    command.use_ipv6 = False

    with patch('django.core.servers.basehttp.run', side_effect=OSError(errno.EACCES, 'Permission denied')):

        with pytest.raises(SystemExit):
            command.inner_run(use_threading=True)

        command.stderr.write.assert_called_once_with("Error: You don't have permission to access that port.")

def test_inner_run_keyboard_interrupt(command):
    command.stdout = MagicMock()
    command.get_handler = MagicMock(return_value='handler')
    command.check = MagicMock()
    command.check_migrations = MagicMock()
    command.port = 8000
    command.addr = '127.0.0.1'
    command.protocol = 'http'
    command.use_ipv6 = False

    with patch('django.core.servers.basehttp.run', side_effect=KeyboardInterrupt):
        with pytest.raises(SystemExit):
            command.inner_run(use_threading=True)

def test_inner_run_with_shutdown_message(command):
    command.stdout = MagicMock()
    command.get_handler = MagicMock(return_value='handler')
    command.check = MagicMock()
    command.check_migrations = MagicMock()
    command.port = 8000
    command.addr = '127.0.0.1'
    command.protocol = 'http'
    command.use_ipv6 = False

    with patch('django.core.servers.basehttp.run', side_effect=KeyboardInterrupt):
        with patch('sys.exit') as mock_exit:
            command.inner_run(use_threading=True, shutdown_message="Server shutting down...")

        command.stdout.write.assert_called_with("Server shutting down...")
        mock_exit.assert_called_once_with(0)