import pytest
from django.core.management.base import CommandError

def test_command_error_init():
    # Test default initialization
    error = CommandError("An error occurred")
    assert error.returncode == 1
    assert str(error) == "An error occurred"
    
    # Test custom return code
    error_with_code = CommandError("Another error", returncode=2)
    assert error_with_code.returncode == 2
    assert str(error_with_code) == "Another error"
    
    # Test with additional args
    error_with_args = CommandError("Error with extra args", returncode=3, extra_arg="extra")
    assert error_with_args.returncode == 3
    assert str(error_with_args) == "Error with extra args"