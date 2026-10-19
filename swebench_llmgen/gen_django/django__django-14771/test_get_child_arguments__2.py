import os
import pytest
import sys
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_with_script_exists(monkeypatch):
    # Arrange
    script_name = 'test_script.py'
    sys.argv = [script_name]
    monkeypatch.setattr('sys.executable', 'python')
    
    # Create a dummy script file
    with open(script_name, 'w') as f:
        f.write("print('Hello World')")

    # Act
    args = get_child_arguments()

    # Assert
    assert args == ['python', '-Wdefault', script_name]

    # Cleanup
    os.remove(script_name)

def test_get_child_arguments_with_script_not_exists(monkeypatch):
    # Arrange
    nonexistent_script = 'nonexistent_script.py'
    sys.argv = [nonexistent_script]
    monkeypatch.setattr('sys.executable', 'python')

    # Act / Assert
    with pytest.raises(RuntimeError, match=f'Script {nonexistent_script} does not exist.'):
        get_child_arguments()

def test_get_child_arguments_with_exe_exists(monkeypatch):
    # Arrange
    exe_script = 'test_script.exe'
    existing_exe = f'{exe_script}.exe'
    sys.argv = [exe_script]
    monkeypatch.setattr('sys.executable', 'python')

    # Simulate that the executable exists
    monkeypatch.setattr('pathlib.Path.exists', lambda _: True)

    # Act
    args = get_child_arguments()

    # Assert
    assert args == [existing_exe]

def test_get_child_arguments_with_module_spec(monkeypatch):
    # Arrange
    sys.argv = ['-m', 'django']
    monkeypatch.setattr('sys.executable', 'python')
    
    # Act
    args = get_child_arguments()

    # Assert
    assert args == ['python', '-Wdefault', '-m', 'django']