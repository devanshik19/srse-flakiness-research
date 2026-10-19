import pytest
import sys
import os
import __main__
from pathlib import Path
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_with_module_name():
    """Test get_child_arguments when starting a module with -m option."""
    original_spec = getattr(__main__, '__spec__', None)
    __main__.__spec__ = type('spec', (), {'name': 'my_module', 'parent': None})()

    sys.argv = ['my_module.py', 'arg1', 'arg2']
    result = get_child_arguments()

    expected_args = [sys.executable, '-m', 'my_module', 'arg1', 'arg2']
    assert result == expected_args

    # Restore original __spec__
    __main__.__spec__ = original_spec

def test_get_child_arguments_with_parent_module():
    """Test get_child_arguments when starting a module with parent."""
    original_spec = getattr(__main__, '__spec__', None)
    __main__.__spec__ = type('spec', (), {'name': '__main__', 'parent': 'my_parent_module'})()

    sys.argv = ['my_script.py', 'arg1']
    result = get_child_arguments()

    expected_args = [sys.executable, '-m', 'my_parent_module', 'arg1']
    assert result == expected_args

    # Restore original __spec__
    __main__.__spec__ = original_spec

def test_get_child_arguments_with_nonexistent_script():
    """Test get_child_arguments when script does not exist."""
    sys.argv = ['nonexistent_script.py']

    with pytest.raises(RuntimeError, match='Script nonexistent_script.py does not exist.'):
        get_child_arguments()

def test_get_child_arguments_with_executable_suffix():
    """Test get_child_arguments when the script exists with .exe suffix."""
    script_name = 'my_script.exe'
    os.mknod(script_name)  # Create an empty file to simulate the executable

    try:
        sys.argv = [script_name]
        result = get_child_arguments()

        expected_args = [sys.executable] + [script_name]
        assert result == expected_args
    finally:
        os.remove(script_name)  # Clean up the created file

def test_get_child_arguments_with_script_suffix():
    """Test get_child_arguments when script exists with -script.py suffix."""
    script_name = 'my_script-script.py'
    os.mknod(script_name)  # Create an empty file to simulate the script

    try:
        sys.argv = ['my_script.py']
        result = get_child_arguments()

        expected_args = [sys.executable] + [script_name]
        assert result == expected_args
    finally:
        os.remove(script_name)  # Clean up the created file

def test_get_child_arguments_with_normal_script():
    """Test get_child_arguments with a normal script."""
    script_name = 'my_script.py'
    os.mknod(script_name)  # Create an empty file to simulate the script

    try:
        sys.argv = [script_name, 'arg1', 'arg2']
        result = get_child_arguments()

        expected_args = [sys.executable, script_name, 'arg1', 'arg2']
        assert result == expected_args
    finally:
        os.remove(script_name)  # Clean up the created file