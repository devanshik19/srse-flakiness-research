import errno
import os
import socket
import sys
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.servers.basehttp import run
from django.utils import autoreload
import pytest
from unittest.mock import patch, MagicMock

class TestCommandInnerRun:
    def setup_method(self):
        self.command = Command()
        self.command.stdout = MagicMock()
        self.command.stderr = MagicMock()

    @patch('django.core.servers.basehttp.run')
    @patch('django.core.management.commands.runserver.Command.get_handler')
    @patch('django.core.management.commands.runserver.Command.check')
    @patch('django.core.management.commands.runserver.Command.check_migrations')
    @patch('django.utils.autoreload.raise_last_exception')
    def test_inner_run_normal_flow(self, mock_raise_last_exception, mock_check_migrations, mock_check, mock_get_handler, mock_run):
        mock_get_handler.return_value = MagicMock()
        options = {
            "use_threading": True,
            "skip_checks": False,
            "shutdown_message": ""
        }
        args = []

        # Call the inner_run method
        self.command.inner_run(*args, **options)

        # Assert that autoreload was called
        mock_raise_last_exception.assert_called_once()

        # Assert checks were performed
        mock_check.assert_called_once()
        mock_check_migrations.assert_called_once()

        # Assert correct logging of server start message
        now = datetime.now().strftime("%B %d, %Y - %X")
        assert self.command.stdout.write.call_count == 2
        assert self.command.stdout.write.call_args_list[0][0][0] == now

        # Assert run was called with correct parameters
        mock_run.assert_called_once_with(
            self.command.addr, 
            int(self.command.port), 
            mock_get_handler.return_value, 
            ipv6=self.command.use_ipv6, 
            threading=options["use_threading"], 
            server_cls=self.command.server_cls
        )

    @patch('django.core.servers.basehttp.run')
    @patch('django.core.management.commands.runserver.Command.get_handler')
    def test_inner_run_os_error(self, mock_get_handler, mock_run):
        options = {
            "use_threading": True,
            "skip_checks": True,
            "shutdown_message": ""
        }
        args = []
        mock_get_handler.return_value = MagicMock()
        mock_run.side_effect = OSError(errno.EACCES)

        self.command.inner_run(*args, **options)

        # Assert an error message was printed
        self.command.stderr.write.assert_called_once_with("Error: You don't have permission to access that port.")
        assert os._exit.called

    @patch('django.core.servers.basehttp.run')
    @patch('django.core.management.commands.runserver.Command.get_handler')
    def test_inner_run_keyboard_interrupt(self, mock_get_handler, mock_run):
        options = {
            "use_threading": True,
            "skip_checks": True,
            "shutdown_message": "Shutting down..."
        }
        args = []
        mock_get_handler.return_value = MagicMock()
        mock_run.side_effect = KeyboardInterrupt

        with pytest.raises(SystemExit):  # Catching the exit when sys.exit is called
            self.command.inner_run(*args, **options)

        # Assert shutdown message was printed
        self.command.stdout.write.assert_called_once_with("Shutting down...")