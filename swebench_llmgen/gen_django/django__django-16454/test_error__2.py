import pytest
from django.core.management.base import CommandError
from django.core.management.base import BaseCommand


class CommandParser(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.called_from_command_line = False

    def error(self, message):
        if self.called_from_command_line:
            super().error(message)
        else:
            raise CommandError("Error: %s" % message)


def test_command_parser_error_called_from_command_line(capsys):
    parser = CommandParser()
    parser.called_from_command_line = True
    
    with pytest.raises(SystemExit):  # This checks for a SystemExit from the super().error call
        parser.error("This is a test error message.")
    
    captured = capsys.readouterr()
    assert "This is a test error message." in captured.out


def test_command_parser_error_not_called_from_command_line():
    parser = CommandParser()
    parser.called_from_command_line = False
    
    with pytest.raises(CommandError) as excinfo:
        parser.error("This is a test error message.")
    
    assert str(excinfo.value) == "Error: This is a test error message."