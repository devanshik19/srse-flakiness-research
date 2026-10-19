import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command as RunserverCommand
from django.contrib.auth.models import User
import socket


@pytest.fixture
def command():
    return RunserverCommand()


def test_inner_run_performs_checks(command):
    command.stdout = command.create_string_io()  # Fake stdout for output capturing
    command.stderr = command.create_string_io()  # Fake stderr for error capturing
    options = {
        "use_threading": False,
        "skip_checks": False,
        "shutdown_message": "",
    }
    
    command.inner_run([], options)

    # Assert the output contains expected strings
    output = command.stdout.getvalue()
    assert 'Performing system checks...' in output
    assert 'Django version' in output


def test_inner_run_with_port_in_use(command):
    # Simulate a port in use condition
    options = {
        "use_threading": False,
        "skip_checks": True,
        "shutdown_message": "",
        "port": 8000,  # Assuming port 8000 is in use
    }
    
    command.addr = 'localhost'  # Set addr to localhost
    command.port = 8000  # Set port
    command.get_handler = lambda *args, **kwargs: None  # Avoid running server for this test
    
    with pytest.raises(SystemExit):
        command.inner_run([], options)

    output = command.stderr.getvalue()
    assert "Error: That port is already in use." in output


def test_inner_run_keyboard_interrupt(command):
    options = {
        "use_threading": False,
        "skip_checks": True,
        "shutdown_message": "Server is shutting down...",
    }

    command.get_handler = lambda *args, **kwargs: None  # Avoid running server for this test

    with pytest.raises(SystemExit):  # Simulate a KeyboardInterrupt (CTRL+C)
        command.inner_run([], options)

    output = command.stdout.getvalue()
    assert "Server is shutting down..." in output