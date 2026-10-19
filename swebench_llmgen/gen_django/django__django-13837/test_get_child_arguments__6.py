import sys
import pytest
from pathlib import Path
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_with_django_runserver(monkeypatch):
    # Simulate the condition where the script is run as `python -m django runserver`
    monkeypatch.setattr(sys, 'argv', ['-m', 'django', 'runserver'])
    expected_args = [sys.executable, '-m', 'django']
    assert get_child_arguments() == expected_args

def test_get_child_arguments_with_existing_script(monkeypatch):
    # Create a temporary script in the current directory
    script_path = Path('test_script.py')
    script_path.write_text('# Test script\n')

    # Simulate running the created script
    monkeypatch.setattr(sys, 'argv', [str(script_path)])
    args = get_child_arguments()
    expected_args = [sys.executable] + [str(script_path)]
    assert args == expected_args

    # Cleanup
    script_path.unlink()

def test_get_child_arguments_with_nonexistent_script(monkeypatch):
    # Simulate that the script does not exist
    monkeypatch.setattr(sys, 'argv', ['nonexistent_script'])
    with pytest.raises(RuntimeError, match='Script nonexistent_script does not exist.'):
        get_child_arguments()

def test_get_child_arguments_with_exe_extension(monkeypatch):
    # Create a temporary executable script simulation
    exe_path = Path('test_script.exe')
    exe_path.touch(exist_ok=True)

    # Simulate running the executable script
    monkeypatch.setattr(sys, 'argv', [str(exe_path)])
    args = get_child_arguments()
    expected_args = [str(exe_path)]
    assert args == expected_args

    # Cleanup
    exe_path.unlink()

def test_get_child_arguments_with_script_suffix(monkeypatch):
    # Create a temporary script with the -script.py suffix
    script_with_suffix = Path('test_script-script.py')
    script_with_suffix.write_text('# Test script with suffix\n')

    # Simulate running the script with the suffix
    monkeypatch.setattr(sys, 'argv', [str(script_with_suffix.stem)])
    args = get_child_arguments()
    expected_args = [sys.executable, str(script_with_suffix)]
    assert args == expected_args

    # Cleanup
    script_with_suffix.unlink()