import pytest
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.contrib.auth.models import User
from django.core.management import CommandParser

class MockCommandLineCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.called_from_command_line = True

class MockNonCommandLineCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.called_from_command_line = False

def test_error_called_from_command_line():
    command = MockCommandLineCommand()
    parser = CommandParser()
    parser.called_from_command_line = True
    
    with pytest.raises(SystemExit) as excinfo:
        parser.error("Test error message")
    
    assert excinfo.value.code is not None  # Verify SystemExit is raised with exit code

def test_error_not_called_from_command_line():
    command = MockNonCommandLineCommand()
    parser = CommandParser()
    parser.called_from_command_line = False
    
    with pytest.raises(CommandError) as excinfo:
        parser.error("Test error message")
    
    assert str(excinfo.value) == "Error: Test error message"  # Verify CommandError has the correct message