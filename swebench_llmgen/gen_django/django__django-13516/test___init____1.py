import pytest
from django.core.management.base import CommandError

def test_command_error_init_with_default_returncode():
    error = CommandError("An error occurred")
    assert error.returncode == 1
    assert str(error) == "An error occurred"

def test_command_error_init_with_custom_returncode():
    error = CommandError("Another error occurred", returncode=2)
    assert error.returncode == 2
    assert str(error) == "Another error occurred"