import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command

@pytest.fixture
def command():
    return Command()

def test_inner_run_performs_system_checks(command, monkeypatch):
    options = {
        "use_threading": False,
        "skip_checks": False,
        "shutdown_message": "",
    }
    args = []

    # Capture stdout and stderr
    from io import StringIO
    command.stdout = StringIO()
    command.stderr = StringIO()
    
    # Assuming the check method is part of the command
    command.check = lambda display_num_errors: None
    command.check_migrations = lambda: None
    command.get_version = lambda: "4.0"
    command.protocol = "http"
    command.addr = "127.0.0.1"
    command.port = "8000"
    command._raw_ipv6 = False
    command.get_handler = lambda *args, **options: None
    
    # Run the inner_run method
    command.inner_run(*args, **options)
    
    # Verify output
    output = command.stdout.getvalue()
    assert "Performing system checks..." in output
    assert "Django version 4.0" in output
    assert "Starting development server at http://127.0.0.1:8000/" in output

def test_inner_run_port_in_use(command, monkeypatch):
    options = {
        "use_threading": False,
        "skip_checks": False,
        "shutdown_message": "",
    }
    args = []

    # Simulating an OSError due to port in use
    def raise_oserror(*args, **kwargs):
        raise OSError(errno.EADDRINUSE, "Address already in use")

    monkeypatch.setattr(command, 'get_handler', lambda *args, **options: None)
    monkeypatch.setattr('django.core.servers.basehttp.run', raise_oserror)

    command.stderr = StringIO()
    
    with pytest.raises(SystemExit):
        command.inner_run(*args, **options)

    error_output = command.stderr.getvalue()
    assert "Error: That port is already in use." in error_output

def test_inner_run_keyboard_interrupt(command, monkeypatch):
    options = {
        "use_threading": False,
        "skip_checks": False,
        "shutdown_message": "Shutting down...",
    }
    args = []

    monkeypatch.setattr(command, 'get_handler', lambda *args, **options: None)

    # Simulate KeyboardInterrupt
    with pytest.raises(SystemExit):
        command.inner_run(*args, **options)

    assert "Shutting down..." in command.stdout.getvalue()