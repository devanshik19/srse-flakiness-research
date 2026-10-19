import errno
import os
import socket
import sys
from datetime import datetime
import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command

@pytest.fixture
def command():
    return Command()

def test_inner_run_system_checks(command, monkeypatch):
    # Mock stdout and stderr to capture output
    class MockStdout:
        def write(self, msg):
            self.messages.append(msg)

    class MockStderr(MockStdout):
        pass

    command.stdout = MockStdout()
    command.stderr = MockStderr()
    command.messages = []

    # Mock the required functions
    def mock_check(*args, **kwargs):
        return True

    def mock_check_migrations(*args, **kwargs):
        return True

    def mock_get_handler(*args, **kwargs):
        return lambda *args, **kwargs: None

    monkeypatch.setattr(command, 'check', mock_check)
    monkeypatch.setattr(command, 'check_migrations', mock_check_migrations)
    monkeypatch.setattr(command, 'get_handler', mock_get_handler)
    monkeypatch.setattr(command, 'run', lambda addr, port, handler, **options: None)

    options = {'use_threading': False, 'shutdown_message': ''}
    command.addr = '127.0.0.1'
    command.port = 8000
    command.protocol = 'http'

    command.inner_run([], options)

    assert "Performing system checks..." in ''.join(command.messages)
    assert "Django version" in ''.join(command.messages)
    assert "Starting development server at http://127.0.0.1:8000/" in ''.join(command.messages)

def test_inner_run_os_error_permission_denied(command, monkeypatch):
    class MockStderr:
        def write(self, msg):
            self.error_message = msg

    command.stderr = MockStderr()

    def mock_run(addr, port, handler, **options):
        raise OSError(errno.EACCES)

    monkeypatch.setattr(command, 'run', mock_run)

    options = {'use_threading': False, 'shutdown_message': ''}
    command.addr = '127.0.0.1'
    command.port = 8000

    with pytest.raises(SystemExit):
        command.inner_run([], options)

    assert "You don't have permission to access that port." in command.stderr.error_message

def test_inner_run_keyboard_interrupt(command, monkeypatch):
    options = {'use_threading': False, 'shutdown_message': 'Server is shutting down...'}
    command.addr = '127.0.0.1'
    command.port = 8000

    def mock_run(addr, port, handler, **options):
        raise KeyboardInterrupt

    monkeypatch.setattr(command, 'run', mock_run)

    with pytest.raises(SystemExit):
        command.inner_run([], options)

    assert command.stdout.messages[-1] == options['shutdown_message']