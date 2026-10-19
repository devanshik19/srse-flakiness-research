import pytest
import sys
from django.core.management import CommandError
from django.contrib.auth.models import User
from django.core.management.commands.runserver import Command


@pytest.fixture
def command():
    return Command()


def test_inner_run_performs_system_checks(command, monkeypatch):
    monkeypatch.setattr(command.stdout, 'write', lambda x: x)  # Mock stdout write
    monkeypatch.setattr(command, 'check', lambda display_num_errors: None)
    monkeypatch.setattr(command, 'check_migrations', lambda: None)
    monkeypatch.setattr(command, 'get_handler', lambda *args, **options: None)
    monkeypatch.setattr(command, 'run', lambda addr, port, handler, ipv6, threading, server_cls: None)

    options = {
        'use_threading': True,
        'shutdown_message': '',
    }

    command.addr = '127.0.0.1'
    command.port = '8000'
    command.protocol = 'http'
    command._raw_ipv6 = False
    command.inner_run(*[], **options)

    assert command.stdout.write.call_count == 4  # Expecting 4 calls to write


def test_inner_run_with_port_in_use(command, monkeypatch):
    monkeypatch.setattr(command.stdout, 'write', lambda x: x)
    monkeypatch.setattr(command.stderr, 'write', lambda x: x)

    # Simulating OSError for port already in use
    def raise_oserror(*args, **kwargs):
        class MockOSError(Exception):
            errno = errno.EADDRINUSE
        raise MockOSError()

    monkeypatch.setattr(command, 'get_handler', lambda *args, **options: None)
    monkeypatch.setattr(command, 'run', raise_oserror)

    options = {
        'use_threading': True,
        'shutdown_message': '',
    }

    command.addr = '127.0.0.1'
    command.port = '8000'

    with pytest.raises(SystemExit):  # Expecting an exit due to error
        command.inner_run(*[], **options)

    command.stderr.write.assert_called_once_with("Error: That port is already in use.")


def test_inner_run_keyboard_interrupt(command, monkeypatch):
    monkeypatch.setattr(command.stdout, 'write', lambda x: x)

    # Simulating KeyboardInterrupt
    monkeypatch.setattr(sys, 'exit', lambda x: x)  # Mocking sys.exit to prevent actual exit

    options = {
        'use_threading': False,
        'shutdown_message': 'Shutting down server...',
    }

    command.addr = '127.0.0.1'
    command.port = '8000'

    with pytest.raises(SystemExit):  # Mock exit; the code raises SystemExit
        command.inner_run(*[], **options)

    command.stdout.write.assert_called_with('Shutting down server...')