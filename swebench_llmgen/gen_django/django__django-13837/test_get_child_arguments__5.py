import sys
import pytest
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_runserver(monkeypatch):
    # Simulate running the server with `python -m django runserver`
    monkeypatch.setattr(sys, 'argv', ['-m', 'django', 'runserver'])
    
    result = get_child_arguments()
    
    assert result[0] == sys.executable
    assert result[1] == '-Wd'  # Check for warning options parsing
    assert result[2] == '-m'
    assert result[3] == 'django'
    assert result[4:] == ['runserver']

def test_get_child_arguments_non_existent_script(monkeypatch):
    # Simulate a script that does not exist
    fake_script = 'invalid_script.py'
    monkeypatch.setattr(sys, 'argv', [fake_script])
    monkeypatch.setattr('pathlib.Path.exists', lambda p: False)

    with pytest.raises(RuntimeError, match=f'Script {fake_script} does not exist.'):
        get_child_arguments()

def test_get_child_arguments_win_exe(monkeypatch):
    # Simulate a scenario where executable exists with .exe suffix
    script_name = 'test_script.py'
    exe_path = script_name + '.exe'
    
    def mock_exists(path):
        return path.name == exe_path

    monkeypatch.setattr(sys, 'argv', [script_name])
    monkeypatch.setattr('pathlib.Path.exists', mock_exists)
    
    result = get_child_arguments()
    
    assert result[0] == exe_path
    assert result[1:] == []

def test_get_child_arguments_win_script(monkeypatch):
    # Simulate a scenario where Python script exists with -script.py suffix
    script_name = 'test_script.py'
    script_path = script_name + '-script.py'
    
    def mock_exists(path):
        return path.name == script_path

    monkeypatch.setattr(sys, 'argv', [script_name])
    monkeypatch.setattr('pathlib.Path.exists', mock_exists)
    
    result = get_child_arguments()
    
    assert result[0] == sys.executable
    assert result[1:] == [script_path]