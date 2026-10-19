import pytest
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class CommandParser(BaseCommand):
    def __init__(self):
        super().__init__()
        self.called_from_command_line = True

    def parse_args(self, args, namespace):
        # Dummy implementation for the sake of testing
        return args

    def error(self, message):
        if self.called_from_command_line:
            super().error(message)
        else:
            raise CommandError("Error: %s" % message)

def test_error_called_from_command_line(capsys):
    parser = CommandParser()
    message = "This is an error message"
    
    parser.error(message)
    
    captured = capsys.readouterr()
    assert "This is an error message" in captured.err

def test_error_not_called_from_command_line():
    parser = CommandParser()
    parser.called_from_command_line = False
    message = "This is an error message"

    with pytest.raises(CommandError) as excinfo:
        parser.error(message)

    assert str(excinfo.value) == "Error: This is an error message"