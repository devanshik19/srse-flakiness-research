import sys
import pytest
from pathlib import Path
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_existing_script():
    # Simulate an existing script file
    script_name = "test_script.py"
    script_path = Path(script_name)
    with open(script_path, 'w') as f:
        f.write("# Test script")
    
    sys.argv = [str(script_path), 'arg1', 'arg2']  # Set up sys.argv
    args = get_child_arguments()
    
    assert args[0] == sys.executable
    assert args[1] == '-W' + str(sys.warnoptions[0]) if sys.warnoptions else args[1]  # Check warning options
    assert args[2] == '-m' + str(__main__.__spec__.name) if getattr(__main__, '__spec__', None) else args[2]  # Check if '-m' version exists
    assert args[3:] == ['arg1', 'arg2']  # Check additional arguments
    
    # Clean up
    script_path.unlink()

def test_get_child_arguments_exe_entrypoint_exists(monkeypatch):
    # Simulate the case where .exe exists
    sys.argv = ["script"]
    py_script = Path("script.py")
    
    # Create an exe file
    exe_script = py_script.with_suffix('.exe')
    exe_script.touch()  # Create an empty executable script
    
    result = get_child_arguments()
    
    assert result[0] == str(exe_script)  # Ensure the exe entry point is returned
    assert result[1:] == []  # No arguments expected as per script execution
    
    # Clean up
    exe_script.unlink()
    py_script.unlink()

def test_get_child_arguments_missing_script():
    sys.argv = ["missing_script.py"]

    with pytest.raises(RuntimeError, match='Script missing_script.py does not exist.'):
        get_child_arguments()