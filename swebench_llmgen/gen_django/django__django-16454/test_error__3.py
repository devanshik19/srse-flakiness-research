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

def test_command_parser_error_called_from_command_line():
    parser = CommandParser()
    parser.called_from_command_line = True
    with pytest.raises(SystemExit) as excinfo:
        parser.error("Test message")
    assert excinfo.value.code != 0  # Ensure it raises SystemExit

def test_command_parser_error_not_called_from_command_line():
    parser = CommandParser()
    parser.called_from_command_line = False
    with pytest.raises(CommandError) as excinfo:
        parser.error("Test message")
    assert str(excinfo.value) == "Error: Test message"