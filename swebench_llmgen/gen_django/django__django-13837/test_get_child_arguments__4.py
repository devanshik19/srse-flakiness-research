import pytest
import sys
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_valid_script(django_main_script):
    # Simulate the scenario where we run the server with 'python -m django runserver'
    sys.argv = ["manage.py", "runserver"]
    assert get_child_arguments() == [sys.executable, '-W', *sys.warnoptions, '-m', 'django', 'runserver']

def test_get_child_arguments_exe_entrypoint(monkeypatch):
    # Simulate a situation where the script has a .exe counterpart on Windows
    sys.argv = ["script.exe"]
    exe_path = "script.exe"  # Assuming this file exists in the context of the test
    monkeypatch.setattr("pathlib.Path.exists", lambda self: self.name == "script.exe")
    monkeypatch.setattr("pathlib.Path.with_suffix", lambda self, suffix: Path(self.stem + suffix))
    
    result = get_child_arguments()
    assert result == [exe_path] + sys.argv[1:]

def test_get_child_arguments_script_entrypoint(monkeypatch):
    # Simulate a situation where the script has a '-script.py' counterpart
    sys.argv = ["script.py"]
    script_path = "script-script.py"  # Assuming this file exists in the context of the test
    monkeypatch.setattr("pathlib.Path.exists", lambda self: self.name in ["script.py", "script-script.py"])
    monkeypatch.setattr("pathlib.Path.with_name", lambda self, name: Path(name))
    
    result = get_child_arguments()
    assert result == [sys.executable, '-W', *sys.warnoptions, script_path] + sys.argv[1:]

def test_get_child_arguments_nonexistent_script():
    # Test when the script does not exist
    sys.argv = ["nonexistent_script.py"]
    
    with pytest.raises(RuntimeError, match='Script nonexistent_script.py does not exist.'):
        get_child_arguments()