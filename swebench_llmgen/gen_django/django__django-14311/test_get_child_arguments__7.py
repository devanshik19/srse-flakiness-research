import sys
import pytest
from pathlib import Path
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_existing_script():
    # Test case where the script exists and returns args with the script
    sys.argv = ['test_script.py', 'arg1', 'arg2']
    Path('test_script.py').touch()  # Simulate the existence of the script
    args = get_child_arguments()
    expected_args = [sys.executable, '-Wdefault', 'test_script.py', 'arg1', 'arg2']
    assert args == expected_args

def test_get_child_arguments_no_script():
    # Test case where the script does not exist, checking for RuntimeError
    sys.argv = ['non_existing_script.py']
    with pytest.raises(RuntimeError, match='Script non_existing_script.py does not exist.'):
        get_child_arguments()

def test_get_child_arguments_existing_exe():
    # Test case where an executable with .exe suffix exists
    sys.argv = ['test_script.py']
    exe_script = Path('test_script.py.exe')
    exe_script.touch()  # Simulate the existence of the .exe file
    args = get_child_arguments()
    expected_args = [exe_script, '']
    assert args == expected_args

def test_get_child_arguments_existing_script_suffix():
    # Test case where a script with -script.py suffix exists
    sys.argv = ['test_script.py']
    script_suffix = Path('test_script-script.py')
    script_suffix.touch()  # Simulate the existence of the script with suffix
    args = get_child_arguments()
    expected_args = [sys.executable, '-Wdefault', str(script_suffix), '']
    assert args == expected_args