import os
import errno
import sys
import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command

@pytest.fixture
def command():
    return Command()

def test_inner_run_perform_system_checks(command, capsys):
    options = {
        'use_threading': True,
        'shutdown_message': '',
    }
    args = []
    
    command.inner_run(*args, **options)

    captured = capsys.readouterr()
    assert "Performing system checks..." in captured.out

def test_inner_run_start_server(command, monkeypatch, capsys):
    options = {
        'use_threading': True,
        'shutdown_message': '',
    }
    args = []
    
    def mock_get_handler(*args, **options):
        return lambda env, start_response: start_response('200 OK', [('Content-Type', 'text/plain')])
    
    monkeypatch.setattr(command, 'get_handler', mock_get_handler)
    
    command.addr = '127.0.0.1'
    command.port = 8000
    command.protocol = 'http'
    command.stdout = sys.stdout
    command.stderr = sys.stderr
    
    command.inner_run(*args, **options)

    captured = capsys.readouterr()
    assert "Django version" in captured.out
    assert "Starting development server at http://127.0.0.1:8000/" in captured.out

def test_inner_run_oserror_permission_denied(command, monkeypatch, capsys):
    options = {
        'use_threading': True,
        'shutdown_message': '',
    }
    args = []

    command.addr = '127.0.0.1'
    command.port = 8000

    def mock_get_handler(*args, **options):
        raise OSError(errno.EACCES, "Permission denied")

    monkeypatch.setattr(command, 'get_handler', mock_get_handler)

    with pytest.raises(SystemExit):
        command.inner_run(*args, **options)
    
    captured = capsys.readouterr()
    assert "Error: You don't have permission to access that port." in captured.err

def test_inner_run_keyboard_interrupt(command, monkeypatch, capsys):
    options = {
        'use_threading': True,
        'shutdown_message': 'Shutting down!',
    }
    args = []

    def mock_get_handler(*args, **options):
        raise KeyboardInterrupt()

    monkeypatch.setattr(command, 'get_handler', mock_get_handler)

    with pytest.raises(SystemExit):
        command.inner_run(*args, **options)

    captured = capsys.readouterr()
    assert "Shutting down!" in captured.out