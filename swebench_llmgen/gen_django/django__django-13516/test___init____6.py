import pytest
from django.core.management.base import CommandError

def test_command_error_init():
    # Test with default returncode
    error = CommandError("An error occurred")
    assert error.returncode == 1

    # Test with a custom returncode
    error = CommandError("Another error occurred", returncode=2)
    assert error.returncode == 2

    # Test with additional arguments
    error = CommandError("Yet another error", returncode=3, additional_info="some_info")
    assert error.returncode == 3