import pytest
from django.core.management.base import CommandError
from django.core.management import CommandParser

class TestCommandParser:

    def test_error_called_from_command_line(self, capsys):
        # Mock the CommandParser to set called_from_command_line to True
        parser = CommandParser()
        parser.called_from_command_line = True

        # Call the error method with a sample message
        parser.error("Test error message")

        # Capture output and check if it was sent to the standard error
        captured = capsys.readouterr()
        assert "Test error message" in captured.err

    def test_error_not_called_from_command_line(self):
        # Mock the CommandParser to set called_from_command_line to False
        parser = CommandParser()
        parser.called_from_command_line = False

        # Call error method and assert that it raises CommandError
        with pytest.raises(CommandError, match="Error: Test error message"):
            parser.error("Test error message")