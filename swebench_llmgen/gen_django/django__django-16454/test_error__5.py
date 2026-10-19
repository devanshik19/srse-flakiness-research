import pytest
from django.core.management.base import CommandError
from django.core.management import BaseCommand

class CommandParser(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.called_from_command_line = False

    def error(self, message):
        if self.called_from_command_line:
            super().error(message)
        else:
            raise CommandError("Error: %s" % message)

def test_error_called_from_command_line():
    parser = CommandParser()
    parser.called_from_command_line = True
    with pytest.raises(SystemExit):  # Catching SystemExit for cmd error messages
        parser.error("This is a test error message.")
    
def test_error_not_called_from_command_line():
    parser = CommandParser()
    parser.called_from_command_line = False
    with pytest.raises(CommandError) as excinfo:
        parser.error("This is a test error message.")
    
    assert str(excinfo.value) == "Error: This is a test error message."