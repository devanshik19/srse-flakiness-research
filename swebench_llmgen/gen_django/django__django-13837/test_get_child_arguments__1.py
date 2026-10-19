import sys
import pytest
import django
from pathlib import Path
from django.contrib.auth.models import User

def test_get_child_arguments_runserver(monkeypatch):
    # Simulate the scenario when Django is run with `python -m django runserver`
    monkeypatch.setattr(sys, 'argv', ['python', '-m', 'django', 'runserver'])
    
    result = get_child_arguments()
    assert result[0] == sys.executable
    assert result[1] == '-W%s' % str()
    assert result[2] == '-m'
    assert result[3] == 'django'

def test_get_child_arguments_non_existing_script(monkeypatch):
    # Simulate a scenario with a non-existing script
    fake_script_path = Path('/fake/path/script.py')
    monkeypatch.setattr(sys, 'argv', [str(fake_script_path)])
    
    with pytest.raises(RuntimeError) as excinfo:
        get_child_arguments()
    assert 'Script' in str(excinfo.value)

def test_get_child_arguments_with_exe_suffix(monkeypatch):
    # Simulate the scenario where the .exe version of the script exists
    original_script = Path(sys.argv[0])
    executable_script = original_script.with_suffix('.exe')
    
    monkeypatch.setattr(sys, 'argv', [str(original_script)])
    monkeypatch.setattr(executable_script, 'exists', lambda: True)

    result = get_child_arguments()
    assert result[0] == str(executable_script)
    
def test_get_child_arguments_with_script_suffix(monkeypatch):
    # Simulate the scenario where the -script.py version of the script exists
    original_script = Path(sys.argv[0])
    script_versioned_path = original_script.with_name(f"{original_script.name}-script.py")
    
    monkeypatch.setattr(sys, 'argv', [str(original_script)])
    monkeypatch.setattr(script_versioned_path, 'exists', lambda: True)

    result = get_child_arguments()
    assert result[0] == sys.executable
    assert script_versioned_path in result
    
def test_get_child_arguments_standard(monkeypatch):
    # Simulate normal operation where the script exists
    valid_script_path = Path(sys.argv[0])
    monkeypatch.setattr(sys, 'argv', [str(valid_script_path)])

    monkeypatch.setattr(valid_script_path, 'exists', lambda: True)
    result = get_child_arguments()
    
    assert result[0] == sys.executable
    assert result[1:] == sys.argv[1:]