import pytest
from io import StringIO
from django.core.management import CommandError
from django.core.management.base import BaseCommand


class TestBaseCommand(BaseCommand):

    def handle(self, *args, **options):
        return "Command executed."


@pytest.fixture
def command():
    return TestBaseCommand(stdout=StringIO(), stderr=StringIO(), no_color=False, force_color=False)


def test_execute_success(command):
    output = command.execute('arg1', 'arg2', {'skip_checks': True})
    assert output == "Command executed."


def test_execute_no_color(command):
    command.execute('arg1', 'arg2', {'no_color': True})
    assert command.style is None


def test_execute_force_color(command):
    command.execute('arg1', 'arg2', {'force_color': True})
    assert command.style


def test_execute_conflicting_color_options(command):
    with pytest.raises(CommandError, match=r"The --no-color and --force-color options can't be used together."):
        command.execute('arg1', 'arg2', {'force_color': True, 'no_color': True})


def test_execute_stdout_redirect(command):
    output_stream = StringIO()
    command.execute('arg1', 'arg2', {'stdout': output_stream})
    assert command.stdout is output_stream


def test_execute_stderr_redirect(command):
    error_stream = StringIO()
    command.execute('arg1', 'arg2', {'stderr': error_stream})
    assert command.stderr is error_stream


def test_execute_rerequires_checks(command):
    command.requires_system_checks = True
    command.execute('arg1', 'arg2', {'skip_checks': False})
    assert True  # checking if no exception is raised


def test_execute_output_transaction(command):
    command.output_transaction = True
    command.execute('arg1', 'arg2', {'database': 'default'})
    # Additional checks related to SQL transaction output can be asserted here