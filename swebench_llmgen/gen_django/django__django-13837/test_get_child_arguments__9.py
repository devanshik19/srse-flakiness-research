import sys
import os
import pytest
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments(monkeypatch):
    # Case 1: Running with 'python -m django runserver'
    monkeypatch.setattr(sys, 'argv', ['python', '-m', 'django', 'runserver', 'arg1', 'arg2'])
    assert get_child_arguments() == ['python', '-W{}'.format(o) for o in sys.warnoptions] + ['-m', 'django', 'runserver', 'arg1', 'arg2']

    # Case 2: Script doesn’t exist but has exe equivalent
    script_path = os.path.join(os.getcwd(), 'non_existing.py')
    exe_path = script_path + '.exe'
    monkeypatch.setattr(sys, 'argv', [script_path, 'arg1', 'arg2'])
    monkeypatch.setattr(os.path, 'exists', lambda path: path == exe_path)
    assert get_child_arguments() == [exe_path, 'arg1', 'arg2']

    # Case 3: Script doesn’t exist but has -script.py equivalent
    script_entrypoint = os.path.join(os.getcwd(), 'non_existing-script.py')
    monkeypatch.setattr(sys, 'argv', [script_path, 'arg1', 'arg2'])
    monkeypatch.setattr(os.path, 'exists', lambda path: path == script_entrypoint)
    assert get_child_arguments() == ['python', '-W{}'.format(o) for o in sys.warnoptions] + [script_entrypoint, 'arg1', 'arg2']

    # Case 4: Executable exists, normal execution
    monkeypatch.setattr(os.path, 'exists', lambda path: False)
    monkeypatch.setattr(os, 'path', lambda path: False)
    with pytest.raises(RuntimeError) as excinfo:
        get_child_arguments()
    assert 'Script non_existing.py does not exist.' in str(excinfo.value)

    # Case 5: Default case, script exists
    monkeypatch.setattr(os.path, 'exists', lambda path: True)
    monkeypatch.setattr(sys, 'argv', ['existing_script.py', 'arg1', 'arg2'])
    assert get_child_arguments() == ['python', '-W{}'.format(o) for o in sys.warnoptions] + ['existing_script.py', 'arg1', 'arg2']