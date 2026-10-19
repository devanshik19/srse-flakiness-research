import pytest
from django.core.management import CommandError
from django.contrib.auth.models import User
from django.core.management.commands.runserver import Command

def test_inner_run_without_checks(mocker):
    command = Command()
    options = {
        "use_threading": False,
        "skip_checks": True,
        "shutdown_message": "",
    }
    mocker.patch.object(command, 'stdout.write')
    mocker.patch.object(command, 'check_migrations')
    mocker.patch.object(command, 'get_handler', return_value=None)
    mocker.patch('django.core.servers.basehttp.run')

    command.inner_run([], options)

    command.check_migrations.assert_called_once()
    assert command.stdout.write.call_count == 2  # Check date and server start message


def test_inner_run_with_checks(mocker):
    command = Command()
    options = {
        "use_threading": False,
        "skip_checks": False,
        "shutdown_message": "",
    }
    mocker.patch.object(command, 'stdout.write')
    mocker.patch.object(command, 'check')
    mocker.patch.object(command, 'check_migrations')
    mocker.patch.object(command, 'get_handler', return_value=None)
    mocker.patch('django.core.servers.basehttp.run')

    command.inner_run([], options)

    command.check.assert_called_once()
    command.check_migrations.assert_called_once()
    assert command.stdout.write.call_count == 2  # Check date and server start message


def test_inner_run_with_port_error(mocker):
    command = Command()
    options = {
        "use_threading": False,
        "skip_checks": True,
        "shutdown_message": "",
    }
    mocker.patch.object(command, 'stdout.write')
    mocker.patch.object(command, 'check_migrations')
    mocker.patch('django.core.servers.basehttp.run', side_effect=OSError(errno.EACCES, "Permission denied"))

    with pytest.raises(SystemExit):
        command.inner_run([], options)

    assert "Error: You don't have permission to access that port." in command.stderr.getvalue()


def test_inner_run_with_keyboard_interrupt(mocker):
    command = Command()
    options = {
        "use_threading": False,
        "skip_checks": True,
        "shutdown_message": "Server is shutting down...",
    }
    mocker.patch.object(command, 'stdout.write')
    mocker.patch.object(command, 'check_migrations')
    mocker.patch.object(command, 'get_handler', side_effect=KeyboardInterrupt)

    with pytest.raises(SystemExit):
        command.inner_run([], options)

    command.stdout.write.assert_any_call("Server is shutting down...")