import sys
import pytest
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_script_exists(monkeypatch):
    # Arrange
    test_script_name = 'test_script.py'
    test_script_path = f'{test_script_name}'
    with open(test_script_path, 'w') as test_script:
        test_script.write('# Test script')
    
    monkeypatch.setattr(sys, 'argv', [test_script_name, 'arg1', 'arg2'])

    # Act
    result = get_child_arguments()

    # Assert
    assert result[0].endswith('python')  # Check for the Python executable
    assert result[1] == '-W' + str([])  # Check warning options
    assert result[2:] == ['arg1', 'arg2']  # Check for script args
    os.remove(test_script_path)

def test_get_child_arguments_executable_exists(monkeypatch):
    # Arrange
    test_executable_name = 'test_executable.exe'
    with open(test_executable_name, 'w') as test_executable:
        test_executable.write('Executable content')

    monkeypatch.setattr(sys, 'argv', [test_executable_name])

    # Act
    result = get_child_arguments()

    # Assert
    assert result[0] == test_executable_name  # Check for executable
    os.remove(test_executable_name)

def test_get_child_arguments_no_script_or_executable(monkeypatch):
    # Arrange
    monkeypatch.setattr(sys, 'argv', ['nonexistent_script.py'])

    # Act & Assert
    with pytest.raises(RuntimeError, match='Script nonexistent_script.py does not exist.'):
        get_child_arguments()