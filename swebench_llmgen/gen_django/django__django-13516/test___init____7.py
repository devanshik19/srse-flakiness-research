import pytest
from django.core.management.base import CommandError

def test_command_error_initialization():
    # Test with default returncode
    error = CommandError("An error occurred")
    assert error.returncode == 1

    # Test with a custom returncode
    error_with_custom_returncode = CommandError("Another error", returncode=2)
    assert error_with_custom_returncode.returncode == 2
  
    # Test with multiple arguments
    error_with_multiple_args = CommandError("Error", "additional info", returncode=3)
    assert error_with_multiple_args.returncode == 3