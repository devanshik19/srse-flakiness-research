import pytest
from django.core.management.base import CommandError

def test_command_error_init():
    # Test default initialization
    command_error = CommandError("Some error occurred")
    assert command_error.returncode == 1
    assert str(command_error) == "Some error occurred"

    # Test initialization with custom returncode
    command_error_custom = CommandError("Another error occurred", returncode=2)
    assert command_error_custom.returncode == 2
    assert str(command_error_custom) == "Another error occurred"

    # Test initialization with no arguments
    command_error_no_args = CommandError()
    assert command_error_no_args.returncode == 1
    assert str(command_error_no_args) == ""