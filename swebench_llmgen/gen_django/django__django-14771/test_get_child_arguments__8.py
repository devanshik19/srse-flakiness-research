import sys
import pytest
from pathlib import Path
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_with_module_spec(monkeypatch):
    # Test with __spec__ set to simulate running as a module
    mock_spec = type('spec', (), {'name': '__main__', 'parent': 'test_module'})
    monkeypatch.setattr('__main__', '__spec__', mock_spec)
    monkeypatch.setattr('sys.argv', ['script_name', 'arg1', 'arg2'])
    
    expected_args = [sys.executable, '-m', 'test_module', 'arg1', 'arg2']
    assert get_child_arguments() == expected_args

def test_get_child_arguments_without_spec(monkeypatch):
    # Test without __spec__ and script does not exist
    py_script = Path(sys.argv[0])
    monkeypatch.setattr('__main__', '__spec__', None)
    monkeypatch.setattr('sys.argv', ['script_name', 'arg1', 'arg2'])
    
    # We need to simulate the case where the script doesn't exist
    monkeypatch.setattr(py_script, 'exists', lambda: False)
    
    # Create script path mocks
    exe_entrypoint = py_script.with_suffix('.exe')
    script_entrypoint = py_script.with_name(f'{py_script.name}-script.py')
    
    monkeypatch.setattr(exe_entrypoint, 'exists', lambda: False)
    monkeypatch.setattr(script_entrypoint, 'exists', lambda: False)
    
    with pytest.raises(RuntimeError, match='Script .* does not exist.'):
        get_child_arguments()

def test_get_child_arguments_with_existing_exe(monkeypatch):
    # Test with executable entry point existing
    mock_script = Path(sys.argv[0])
    monkeypatch.setattr('__main__', '__spec__', None)
    monkeypatch.setattr('sys.argv', ['script_name', 'arg1', 'arg2'])

    exe_entrypoint = mock_script.with_suffix('.exe')
    monkeypatch.setattr(mock_script, 'exists', lambda: False)
    monkeypatch.setattr(exe_entrypoint, 'exists', lambda: True)

    assert get_child_arguments() == [exe_entrypoint, 'arg1', 'arg2']

def test_get_child_arguments_with_existing_script(monkeypatch):
    # Test with script entry point existing
    mock_script = Path(sys.argv[0])
    monkeypatch.setattr('__main__', '__spec__', None)
    monkeypatch.setattr('sys.argv', ['script_name', 'arg1', 'arg2'])

    script_entrypoint = mock_script.with_name(f'{mock_script.name}-script.py')
    monkeypatch.setattr(mock_script, 'exists', lambda: False)
    monkeypatch.setattr(script_entrypoint, 'exists', lambda: True)

    assert get_child_arguments() == [sys.executable, script_entrypoint, 'arg1', 'arg2']

def test_get_child_arguments_with_existing_script_no_args(monkeypatch):
    # Test with no additional args
    mock_script = Path(sys.argv[0])
    monkeypatch.setattr('__main__', '__spec__', None)
    monkeypatch.setattr('sys.argv', ['script_name'])

    script_entrypoint = mock_script.with_name(f'{mock_script.name}-script.py')
    monkeypatch.setattr(mock_script, 'exists', lambda: False)
    monkeypatch.setattr(script_entrypoint, 'exists', lambda: True)

    assert get_child_arguments() == [sys.executable, script_entrypoint]