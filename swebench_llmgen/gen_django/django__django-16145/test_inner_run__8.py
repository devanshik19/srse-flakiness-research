import pytest
import socket
import sys
from django.core.management import CommandError
from django.core.management.commands.runserver import Command
from django.conf import settings

@pytest.fixture
def command():
    return Command()

def test_inner_run_performs_checks_and_starts_server(command, monkeypatch, capsys):
    options = {
        "use_threading": True,
        "shutdown_message": "",
        "skip_checks": False,
    }
    
    monkeypatch.setattr(command, "get_handler", lambda *args, **kwargs: None)
    monkeypatch.setattr(command, "check", lambda display_num_errors: None)
    monkeypatch.setattr(command, "check_migrations", lambda: None)
    command.addr = '127.0.0.1'
    command.port = 8000

    command.inner_run([], options)

    captured = capsys.readouterr()
    assert "Performing system checks..." in captured.out
    assert "Django version" in captured.out
    assert "Starting development server at" in captured.out

def test_inner_run_no_checks(command, monkeypatch, capsys):
    options = {
        "use_threading": False,
        "shutdown_message": "",
        "skip_checks": True,
    }
    
    monkeypatch.setattr(command, "get_handler", lambda *args, **kwargs: None)
    monkeypatch.setattr(command, "check_migrations", lambda: None)
    command.addr = '127.0.0.1'
    command.port = 8000

    command.inner_run([], options)

    captured = capsys.readouterr()
    assert "Performing system checks..." not in captured.out

def test_inner_run_handling_OSError(command, monkeypatch, capsys):
    options = {
        "use_threading": True,
        "shutdown_message": "",
        "skip_checks": False,
    }
    
    monkeypatch.setattr(command, "get_handler", lambda *args, **kwargs: None)
    monkeypatch.setattr(command, "check", lambda display_num_errors: None)
    monkeypatch.setattr(command, "check_migrations", lambda: None)
    command.addr = '127.0.0.1'
    command.port = 80  # Assuming some port that might raise due to permission issues
    
    # Simulate permission error
    monkeypatch.setattr(socket, "bind", lambda x: (_ for _ in ()).throw(OSError(errno.EACCES, 'Permission denied')))

    with pytest.raises(SystemExit) as pytest_exit:
        command.inner_run([], options)
    assert pytest_exit.type == SystemExit

    captured = capsys.readouterr()
    assert "Error: You don't have permission to access that port." in captured.stderr

def test_inner_run_keyboard_interrupt(command, monkeypatch, capsys):
    options = {
        "use_threading": True,
        "shutdown_message": "Shutting down...",
        "skip_checks": False,
    }

    monkeypatch.setattr(command, "get_handler", lambda *args, **kwargs: None)
    monkeypatch.setattr(command, "check", lambda display_num_errors: None)
    monkeypatch.setattr(command, "check_migrations", lambda: None)
    command.addr = '127.0.0.1'
    command.port = 8000

    with pytest.raises(SystemExit):
        command.inner_run([], options)
    
    captured = capsys.readouterr()
    assert "Shutting down..." in captured.out