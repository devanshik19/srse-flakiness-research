import pytest
from django.core.management.base import CommandError
from django.core.management import BaseCommand

class CommandParser(BaseCommand):
    def __init__(self):
        super().__init__()
        self.called_from_command_line = False

    def error(self, message):
        if self.called_from_command_line:
            super().error(message)
        else:
            raise CommandError("Error: %s" % message)

def test_command_parser_error_called_from_command_line():
    parser = CommandParser()
    parser.called_from_command_line = True
    with pytest.raises(SystemExit):
        parser.error("This is a test error.")

def test_command_parser_error_not_called_from_command_line():
    parser = CommandParser()
    parser.called_from_command_line = False
    with pytest.raises(CommandError) as exc_info:
        parser.error("This is a test error.")
    assert str(exc_info.value) == "Error: This is a test error."