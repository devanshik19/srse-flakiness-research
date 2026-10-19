import pytest
import sys
import os
from pathlib import Path
from django.contrib.auth.models import User

def test_get_child_arguments(monkeypatch):
    # Test case for when __spec__ is not None and has a parent
    class MockMain:
        __spec__ = type('spec', (), {"parent": "mock_parent"})
    
    monkeypatch.setattr('__main__', MockMain)
    monkeypatch.setattr('sys.argv', ['script.py', 'arg1', 'arg2'])
    assert get_child_arguments() == ['python', '-Wnone', '-m', 'mock_parent', 'arg1', 'arg2']

    # Test case for when Path does not exist and exe file exists
    py_script_path = Path('./script.py')
    
    def mock_exists(path):
        if path == py_script_path:
            return False
        return True
    
    monkeypatch.setattr(py_script_path, 'exists', lambda: False)
    monkeypatch.setattr('Path.exists', mock_exists)
    
    exe_entrypoint_path = Path('./script.exe')
    monkeypatch.setattr(exe_entrypoint_path, 'exists', lambda: True)
    monkeypatch.setattr('sys.executable', 'python')
    
    assert get_child_arguments() == ['script.exe', 'arg1', 'arg2']

    # Test case for when Path exists and sys.argv is used directly
    monkeypatch.setattr(py_script_path, 'exists', lambda: True)
    monkeypatch.setattr('sys.argv', ['script.py', 'arg1', 'arg2'])
    
    assert get_child_arguments() == ['python', '-Wnone', 'script.py', 'arg1', 'arg2']

    # Test case for when neither case is valid
    monkeypatch.setattr(py_script_path, 'exists', lambda: False)
    
    with pytest.raises(RuntimeError) as excinfo:
        get_child_arguments()
    assert 'Script' in str(excinfo.value)