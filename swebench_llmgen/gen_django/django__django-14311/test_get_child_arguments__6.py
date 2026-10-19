import sys
import pytest
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_exists():
    """ Test when the script exists directly. """
    sys.argv = ['test_script.py']
    with open('test_script.py', 'w') as f:
        f.write('print("Hello World")')
    
    args = get_child_arguments()
    assert args == [sys.executable, 'test_script.py']

def test_get_child_arguments_script_script_py():
    """ Test when the script exists as a script file. """
    sys.argv = ['test_script']
    with open('test_script-script.py', 'w') as f:
        f.write('print("Hello World")')
        
    args = get_child_arguments()
    assert args == [sys.executable, 'test_script-script.py']

def test_get_child_arguments_exe():
    """ Test when the script exists with .exe extension. """
    sys.argv = ['test_script']
    with open('test_script.exe', 'w') as f:
        f.write('print("Hello World")')

    args = get_child_arguments()
    assert args == ['test_script.exe']

def test_get_child_arguments_error():
    """ Test when the script does not exist. """
    sys.argv = ['non_existent_script']
    
    with pytest.raises(RuntimeError, match='Script non_existent_script does not exist.'):
        get_child_arguments()