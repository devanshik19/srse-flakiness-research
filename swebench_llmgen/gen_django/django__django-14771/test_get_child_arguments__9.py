import sys
import pytest
import functools
import os
from pathlib import Path

# Import the function to test
from django.utils.autoreload import get_child_arguments

@pytest.fixture
def setup_script_file(tmp_path):
    script_file = tmp_path / "test_script.py"
    script_file.write_text("print('Hello')")
    yield script_file

def test_get_child_arguments_relative_path(setup_script_file):
    sys.argv = [str(setup_script_file), "arg1", "arg2"]
    result = get_child_arguments()
    assert result[0] == sys.executable
    assert result[1] == '-W'
    assert result[2] == 'arg1'
    assert result[3] == 'arg2'
    assert str(setup_script_file) in result

def test_get_child_arguments_executable_exists(monkeypatch, setup_script_file):
    sys.argv = [str(setup_script_file.with_suffix('.exe')), "arg1"]
    # Create a dummy .exe file
    exe_file = setup_script_file.with_suffix('.exe')
    exe_file.write_text("print('Hello')")
    result = get_child_arguments()
    assert result[0] == str(exe_file)
    assert result[1] == 'arg1'

def test_get_child_arguments_no_script_file(monkeypatch):
    sys.argv = ["unknown_script.py"]
    
    with pytest.raises(RuntimeError, match='Script unknown_script.py does not exist.'):
        get_child_arguments()

def test_get_child_arguments_module_spec(monkeypatch):
    from types import ModuleType
    module = ModuleType('__main__', "Test Module")
    module.__spec__ = type("spec", (), {"name": "__main__", "parent": None})()
    monkeypatch.setattr('__main__', module)

    sys.argv = ["script.py", "arg1", "arg2"]
    result = get_child_arguments()
    assert result[0] == sys.executable
    assert len(result) == 4  # Should include executable, '-m', name of the module, and args

def test_get_child_arguments_module_with_parent(monkeypatch):
    from types import ModuleType
    module = ModuleType('__main__', "Test Module")
    module.__spec__ = type("spec", (), {"name": "parent.module", "parent": "parent"})()
    monkeypatch.setattr('__main__', module)

    sys.argv = ["script.py", "arg1"]
    result = get_child_arguments()
    assert result[0] == sys.executable
    assert result[1] == '-m'
    assert result[2] == "parent.module"
    assert result[3] == "arg1"