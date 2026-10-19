import pytest
from django.core.management import call_command
from django.core.management.commands.runserver import Command
from django.contrib.auth.models import User
from django.utils import autoreload

@pytest.fixture
def command():
    return Command()

def test_inner_run_system_checks(command, capsys):
    options = {
        "use_threading": False,
        "skip_checks": False,
        "shutdown_message": "",
    }
    command.check = lambda display_num_errors: None
    command.check_migrations = lambda: None
    command.get_handler = lambda *args, **options: None
    command.addr = "127.0.0.1"
    command.port = "8000"
    command.protocol = "http"
    command.stdout.write = lambda message: None
    command.stderr.write = lambda message: None

    with pytest.raises(SystemExit):
        command.inner_run([], options)

    captured = capsys.readouterr()
    assert "Performing system checks..." in captured.out

def test_inner_run_no_system_checks(command, capsys):
    options = {
        "use_threading": False,
        "skip_checks": True,
        "shutdown_message": "",
    }
    command.check_migrations = lambda: None
    command.get_handler = lambda *args, **options: None
    command.addr = "127.0.0.1"
    command.port = "8000"
    command.protocol = "http"
    command.stdout.write = lambda message: None
    command.stderr.write = lambda message: None

    with pytest.raises(SystemExit):
        command.inner_run([], options)

    captured = capsys.readouterr()
    assert "Performing system checks..." not in captured.out

def test_inner_run_error_handling(command, capsys):
    options = {
        "use_threading": False,
        "skip_checks": False,
        "shutdown_message": "",
    }
    command.check = lambda display_num_errors: None
    command.check_migrations = lambda: None
    command.get_handler = lambda *args, **options: None
    command.addr = "127.0.0.1"
    command.port = "8000"
    command.protocol = "http"
    command.stdout.write = lambda message: None
    command.stderr.write = lambda message: None
    
    # Simulating an OSError
    command.get_handler = lambda *args, **options: (_ for _ in ()).throw(OSError(errno.EACCES))

    with pytest.raises(SystemExit):
        command.inner_run([], options)

    captured = capsys.readouterr()
    assert "You don't have permission to access that port." in captured.err

def test_inner_run_keyboard_interrupt(command, capsys):
    options = {
        "use_threading": False,
        "skip_checks": False,
        "shutdown_message": "",
    }
    command.check = lambda display_num_errors: None
    command.check_migrations = lambda: None
    command.get_handler = lambda *args, **options: None
    command.addr = "127.0.0.1"
    command.port = "8000"
    command.protocol = "http"
    command.stdout.write = lambda message: None
    command.stderr.write = lambda message: None

    with pytest.raises(SystemExit):
        command.inner_run([], options)

    import signal
    signal.raise_signal(signal.SIGINT)  # Simulate KeyboardInterrupt

    captured = capsys.readouterr()
    assert "Quit the server with" in captured.out