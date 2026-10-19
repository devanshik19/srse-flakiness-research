import pytest
from django.core.management import CommandError

def test_command_error_initialization():
    # Test with default return code
    error = CommandError("An error occurred")
    assert error.returncode == 1
    assert str(error) == "An error occurred"

    # Test with a custom return code
    error_with_custom_code = CommandError("Another error occurred", returncode=2)
    assert error_with_custom_code.returncode == 2
    assert str(error_with_custom_code) == "Another error occurred"

    # Test with additional arguments
    error_with_args = CommandError("Error with args", returncode=3, extra_arg="extra")
    assert error_with_args.returncode == 3
    assert str(error_with_args) == "Error with args"

    # Test initialization with no arguments
    error_no_args = CommandError()
    assert error_no_args.returncode == 1
    assert str(error_no_args) == ""