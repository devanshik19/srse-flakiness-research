import pytest
import sys
import os
import __main__
from django.contrib.auth.models import User
from pathlib import Path
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_script_exists():
    sys.argv = ['test_script.py']
    with open('test_script.py', 'w') as f:
        f.write('print("This is a test script.")')
    
    try:
        args = get_child_arguments()
        assert args[0] == sys.executable
        assert args[1] == '-W%s' % (o for o in sys.warnoptions)
        assert 'test_script.py' in args
    finally:
        os.remove('test_script.py')

def test_get_child_arguments_exe_exists(monkeypatch):
    script_name = 'test_script.py'
    exe_name = Path(script_name).with_suffix('.exe')

    sys.argv = [script_name]
    # Create a dummy executable
    with open(exe_name, 'w') as f:
        f.write('print("This is a test executable.")')
    
    monkeypatch.setattr(sys, 'executable', str(exe_name))
    
    try:
        args = get_child_arguments()
        assert args[0] == str(exe_name)
        assert len(args) == 1  # There should be no additional arguments
    finally:
        os.remove(exe_name)

def test_get_child_arguments_script_does_not_exist():
    sys.argv = ['non_existing_script.py']
    
    with pytest.raises(RuntimeError, match='Script non_existing_script.py does not exist.'):
        get_child_arguments()