import pytest
from django.core.management.base import CommandError

def test_command_error_init():
    # Test default initialization
    error = CommandError("An error occurred")
    assert error.returncode == 1
    assert str(error) == "An error occurred"

    # Test custom return code
    error_with_code = CommandError("Custom error", returncode=2)
    assert error_with_code.returncode == 2
    assert str(error_with_code) == "Custom error"

    # Test additional args and kwargs
    error_with_kwargs = CommandError("Another error", returncode=3, custom_arg="value")
    assert error_with_kwargs.returncode == 3
    assert str(error_with_kwargs) == "Another error"