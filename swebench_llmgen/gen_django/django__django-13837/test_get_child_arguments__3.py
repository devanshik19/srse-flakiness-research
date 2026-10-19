import sys
import pytest
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_runserver(monkeypatch):
    # Test when the script is run with 'python -m django runserver'
    monkeypatch.setattr(sys, 'argv', ['python', '-m', 'django', 'runserver'])
    expected_args = ['python', '-Wnone', '-m', 'django']
    assert get_child_arguments() == expected_args

def test_get_child_arguments_non_existent_script(monkeypatch):
    # Test when the sys.argv[0] does not exist
    non_existent_path = 'non_existent_script.py'
    monkeypatch.setattr(sys, 'argv', [non_existent_path])
    monkeypatch.setattr(sys.modules['django.__main__'], '__file__', non_existent_path)
    
    # This should raise a RuntimeError since the script does not exist
    with pytest.raises(RuntimeError, match=f'Script {non_existent_path} does not exist.'):
        get_child_arguments()

def test_get_child_arguments_with_exe_suffix(monkeypatch):
    # Test when there is an executable with .exe suffix
    existing_exe_path = 'script.exe'
    monkeypatch.setattr(sys, 'argv', [existing_exe_path])
    monkeypatch.setattr(sys.modules['django.__main__'], '__file__', existing_exe_path)
    
    # Mocking the return value of exists
    def mock_exists(path):
        return path.name == 'script.exe'

    monkeypatch.setattr(Path, 'exists', mock_exists)

    expected_args = [str(Path(sys.executable).with_suffix('.exe')), *sys.argv[1:]]
    assert get_child_arguments() == expected_args

def test_get_child_arguments_with_script_suffix(monkeypatch):
    # Test with script suffix
    existing_script_path = 'script-script.py'
    monkeypatch.setattr(sys, 'argv', [existing_script_path])
    monkeypatch.setattr(sys.modules['django.__main__'], '__file__', existing_script_path)

    # Mocking the return value of exists
    def mock_exists(path):
        return path.name == 'script-script.py'

    monkeypatch.setattr(Path, 'exists', mock_exists)

    expected_args = [str(Path(sys.executable)), existing_script_path]
    assert get_child_arguments() == expected_args