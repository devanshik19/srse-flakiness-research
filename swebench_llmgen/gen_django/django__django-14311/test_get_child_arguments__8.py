import sys
import pytest
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_script_exists(monkeypatch):
    # Test case where the script exists as expected
    monkeypatch.setattr('sys.argv', ['test_script.py', 'arg1', 'arg2'])
    monkeypatch.setattr('pathlib.Path.exists', lambda s: True)  # Pretend the script exists
    monkeypatch.setattr('pathlib.Path.name', 'test_script')
    
    expected_args = [sys.executable, '-W%s' % o for o in sys.warnoptions] + ['test_script.py', 'arg1', 'arg2']
    assert get_child_arguments() == expected_args

def test_get_child_arguments_exe_exists(monkeypatch):
    # Test case where an .exe version of the script exists
    monkeypatch.setattr('sys.argv', ['test_script.py', 'arg1', 'arg2'])
    monkeypatch.setattr('pathlib.Path.exists', side_effect=lambda: False)  # Pretend the script doesn't exist
    monkeypatch.setattr('pathlib.Path.with_suffix', lambda s: True)  # Pretend .exe exists
    
    expected_args = ['test_script.exe', 'arg1', 'arg2']
    assert get_child_arguments() == expected_args

def test_get_child_arguments_script_script_exists(monkeypatch):
    # Test case where a -script.py version of the script exists
    monkeypatch.setattr('sys.argv', ['test_script.py', 'arg1', 'arg2'])
    monkeypatch.setattr('pathlib.Path.exists', side_effect=lambda: False)  # Pretend original script doesn't exist
    monkeypatch.setattr('pathlib.Path.with_name', lambda s: True)  # Pretend -script.py exists
    
    expected_args = ['test_script-script.py', 'arg1', 'arg2']
    assert get_child_arguments() == expected_args

def test_get_child_arguments_runtime_error(monkeypatch):
    # Test case where the script does not exist and no exe or -script.py exists
    monkeypatch.setattr('sys.argv', ['non_existent_script.py'])
    monkeypatch.setattr('pathlib.Path.exists', lambda s: False)  # Pretend the script doesn't exist
    with pytest.raises(RuntimeError, match='Script non_existent_script.py does not exist.'):
        get_child_arguments()