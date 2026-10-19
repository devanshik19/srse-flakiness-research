import pytest
from django.core.management.base import CommandError
from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.core import checks

class CommandParser(BaseCommand):
    def __init__(self):
        self.called_from_command_line = True

    def error(self, message):
        if self.called_from_command_line:
            super().error(message)
        else:
            raise CommandError("Error: %s" % message)

def test_error_called_from_command_line(capsys):
    parser = CommandParser()
    parser.error("This is a test error message.")
    
    captured = capsys.readouterr()
    assert "This is a test error message." in captured.err

def test_error_not_called_from_command_line():
    parser = CommandParser()
    parser.called_from_command_line = False
    with pytest.raises(CommandError, match="Error: This is a test error message."):
        parser.error("This is a test error message.")