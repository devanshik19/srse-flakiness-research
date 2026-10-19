import pytest
from django.core.management import CommandError
from django.core.management.base import BaseCommand

class CommandParser(BaseCommand):
    def __init__(self):
        self.called_from_command_line = False

    def error(self, message):
        if self.called_from_command_line:
            super().error(message)
        else:
            raise CommandError("Error: %s" % message)

def test_error_called_from_command_line():
    parser = CommandParser()
    parser.called_from_command_line = True
    with pytest.raises(SystemExit) as excinfo:
        parser.error("This is a command line error.")
    assert excinfo.value.code is not None  # Ensure it exits

def test_error_not_called_from_command_line():
    parser = CommandParser()
    parser.called_from_command_line = False
    with pytest.raises(CommandError) as excinfo:
        parser.error("This is not a command line error.")
    assert str(excinfo.value) == "Error: This is not a command line error."