import pytest
from django.core.management.base import CommandError
from django.core.management import BaseCommand

class CommandParser(BaseCommand):
    called_from_command_line = True

    def error(self, message):
        if self.called_from_command_line:
            super().error(message)
        else:
            raise CommandError("Error: %s" % message)

def test_error_called_from_command_line(capfd):
    parser = CommandParser()
    message = "This is a test error message."
    
    parser.error(message)
    
    captured = capfd.readouterr()
    assert message in captured.out

def test_error_not_called_from_command_line():
    parser = CommandParser()
    parser.called_from_command_line = False
    message = "This is a test error message."
    
    with pytest.raises(CommandError) as excinfo:
        parser.error(message)
    
    assert str(excinfo.value) == "Error: %s" % message