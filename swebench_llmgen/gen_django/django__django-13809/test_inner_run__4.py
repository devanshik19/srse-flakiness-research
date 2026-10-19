import errno
import os
import sys
import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command

class MockStdout:
    output = ""

    def write(self, message):
        self.output += message

class MockStderr:
    output = ""

    def write(self, message):
        self.output += message

@pytest.fixture
def command():
    cmd = Command()
    cmd.stdout = MockStdout()
    cmd.stderr = MockStderr()
    cmd.addr = '127.0.0.1'
    cmd.port = '8000'
    cmd.protocol = 'http'
    cmd._raw_ipv6 = False
    cmd.get_handler = lambda *args, **options: None  # Mock handler
    cmd.check = lambda display_num_errors: None  # Mock check
    cmd.check_migrations = lambda: None  # Mock check_migrations
    cmd.get_version = lambda: '3.0'  # Mock version
    cmd.server_cls = None  # Mock server class
    return cmd

def test_inner_run_success(command, monkeypatch):
    monkeypatch.setattr("django.core.servers.basehttp.run", lambda addr, port, handler, ipv6=False, threading=False, server_cls=None: None)
    
    command.inner_run(use_threading=False)
    assert "Performing system checks..." in command.stdout.output
    assert "Django version" in command.stdout.output
    assert "Starting development server at" in command.stdout.output

def test_inner_run_os_error_permission_denied(command, monkeypatch):
    def mock_run(*args, **kwargs):
        raise OSError(errno.EACCES, "Permission denied")

    monkeypatch.setattr("django.core.servers.basehttp.run", mock_run)

    command.inner_run(use_threading=False)
    assert "Error: You don't have permission to access that port." in command.stderr.output

def test_inner_run_os_error_address_in_use(command, monkeypatch):
    def mock_run(*args, **kwargs):
        raise OSError(errno.EADDRINUSE, "Address already in use")

    monkeypatch.setattr("django.core.servers.basehttp.run", mock_run)

    command.inner_run(use_threading=False)
    assert "Error: That port is already in use." in command.stderr.output

def test_inner_run_os_error_address_not_available(command, monkeypatch):
    def mock_run(*args, **kwargs):
        raise OSError(errno.EADDRNOTAVAIL, "Address not available")

    monkeypatch.setattr("django.core.servers.basehttp.run", mock_run)

    command.inner_run(use_threading=False)
    assert "Error: That IP address can't be assigned to." in command.stderr.output

def test_inner_run_keyboard_interrupt(command, monkeypatch):
    def mock_run(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr("django.core.servers.basehttp.run", mock_run)

    command.inner_run(use_threading=False)
    assert command.stdout.output == ""