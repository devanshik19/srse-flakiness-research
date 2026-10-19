import sys
import pytest
from django.contrib.auth.models import User
from pathlib import Path
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_existing_script(monkeypatch):
    # Simulate script execution in __main__
    script_name = 'test_script.py'
    monkeypatch.setattr(sys, 'argv', [script_name])
    
    # Create a mock script for testing
    script_path = Path(script_name)
    script_path.touch()  # Create the script file
    
    args = get_child_arguments()
    
    assert args[0] == sys.executable
    assert args[1] == '-Wnone'  # Default value if no warnings are set
    assert args[2:] == [script_name]

    script_path.unlink()  # Clean up the mock script

def test_get_child_arguments_executable_exists(monkeypatch):
    # Simulate script execution in __main__ with .exe
    script_name = 'test_script.py'
    executable_name = 'test_script.exe'
    monkeypatch.setattr(sys, 'argv', [script_name])

    # Create a mock executable for testing
    executable_path = Path(executable_name)
    executable_path.touch()  # Create the executable file

    # Ensure the .exe file exists
    args = get_child_arguments()
    
    assert args[0] == executable_name
    assert args[1:] == []

    executable_path.unlink()  # Clean up the mock executable

def test_get_child_arguments_script_not_exists(monkeypatch):
    # Simulate script execution where the script does not exist
    script_name = 'non_existing_script.py'
    monkeypatch.setattr(sys, 'argv', [script_name])
    
    with pytest.raises(RuntimeError, match=f'Script {script_name} does not exist.'):
        get_child_arguments()

def test_get_child_arguments_with_python_module(monkeypatch):
    # Simulate running as a Python module
    monkeypatch.setattr(sys, 'argv', ['-m', 'test_module'])
    
    # Mock __main__.__spec__
    class Spec:
        name = '__main__'
        parent = None
        
    monkeypatch.setattr("__main__.__spec__", Spec())
    
    args = get_child_arguments()
    
    assert args[0] == sys.executable
    assert args[1] == '-Wnone'  # Default case for the warning option
    assert args[2] == '-m'
    assert args[3] == 'test_module'