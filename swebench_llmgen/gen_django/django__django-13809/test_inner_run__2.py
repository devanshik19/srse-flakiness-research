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


class Command(BaseCommand):
    help = "Run the Django development server"

    def inner_run(self, *args, **options):
        autoreload.raise_last_exception()

        threading = options['use_threading']
        shutdown_message = options.get('shutdown_message', '')
        quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'

        self.stdout.write("Performing system checks...\n\n")
        self.check(display_num_errors=True)
        self.check_migrations()
        now = datetime.now().strftime('%B %d, %Y - %X')
        self.stdout.write(now)
        self.stdout.write((
            "Django version %(version)s, using settings %(settings)r\n"
            "Starting development server at %(protocol)s://%(addr)s:%(port)s/\n"
            "Quit the server with %(quit_command)s."
        ) % {
            "version": self.get_version(),
            "settings": settings.SETTINGS_MODULE,
            "protocol": self.protocol,
            "addr": '[%s]' % self.addr if self._raw_ipv6 else self.addr,
            "port": self.port,
            "quit_command": quit_command,
        })

        try:
            handler = self.get_handler(*args, **options)
            run(self.addr, int(self.port), handler,
                ipv6=self.use_ipv6, threading=threading, server_cls=self.server_cls)
        except OSError as e:
            ERRORS = {
                errno.EACCES: "You don't have permission to access that port.",
                errno.EADDRINUSE: "That port is already in use.",
                errno.EADDRNOTAVAIL: "That IP address can't be assigned to.",
            }
            error_text = ERRORS.get(e.errno, e)
            self.stderr.write("Error: %s" % error_text)
            os._exit(1)
        except KeyboardInterrupt:
            if shutdown_message:
                self.stdout.write(shutdown_message)
            sys.exit(0)


@pytest.fixture
def command():
    return Command()


def test_inner_run_output(command):
    options = {
        'use_threading': False,
        'shutdown_message': '',
    }
    args = []
    
    with patch.object(command, 'stdout', new_callable=MagicMock()) as mock_stdout, \
         patch.object(command, 'stderr', new_callable=MagicMock()) as mock_stderr, \
         patch('django.core.servers.basehttp.run') as mock_run, \
         patch.object(autoreload, 'raise_last_exception') as mock_raise_last_exception, \
         patch.object(command, 'get_handler', return_value=MagicMock()) as mock_get_handler:
        
        command.inner_run(*args, **options)

        assert mock_stdout.write.call_count >= 3
        assert "Performing system checks..." in [call[0][0] for call in mock_stdout.write.call_args_list]
        assert "Django version" in [call[0][0] for call in mock_stdout.write.call_args_list]
        assert mock_run.call_count == 1


def test_inner_run_oserror(command):
    options = {
        'use_threading': False,
        'shutdown_message': '',
    }
    args = []
    
    with patch.object(command, 'stdout', new_callable=MagicMock()) as mock_stdout, \
         patch.object(command, 'stderr', new_callable=MagicMock()) as mock_stderr, \
         patch('django.core.servers.basehttp.run', side_effect=OSError(errno.EACCES, "Permission denied")):
        
        with pytest.raises(SystemExit):
            command.inner_run(*args, **options)
        
        mock_stderr.write.assert_called_once_with("Error: You don't have permission to access that port.")


def test_inner_run_keyboard_interrupt(command):
    options = {
        'use_threading': False,
        'shutdown_message': 'Shutting down...',
    }
    args = []
    
    with patch('django.core.servers.basehttp.run', side_effect=KeyboardInterrupt):
    
        with pytest.raises(SystemExit):
            command.inner_run(*args, **options)
        
        assert command.stdout.write.call_count == 1
        command.stdout.write.assert_called_with('Shutting down...')