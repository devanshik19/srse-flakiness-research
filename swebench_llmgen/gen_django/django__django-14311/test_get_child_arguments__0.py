import sys
import pytest
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_with_existing_script():
    # Simulate an existing script with .py extension
    sys.argv = ['test_script.py']
    script_path = Path(sys.argv[0])
    script_path.touch()
    
    args = get_child_arguments()
    assert args[0] == sys.executable
    assert args[1:] == sys.argv[1:]

    # Cleanup
    script_path.unlink()

def test_get_child_arguments_with_existing_executable():
    # Simulate an existing executable with .exe extension
    sys.argv = ['test_script.py']
    script_path = Path(sys.argv[0])
    exe_path = script_path.with_suffix('.exe')
    exe_path.touch()

    args = get_child_arguments()
    assert args[0] == exe_path
    assert args[1:] == sys.argv[1:]

    # Cleanup
    exe_path.unlink()

def test_get_child_arguments_with_script_suffix():
    # Simulate a script with the suffix '-script.py' present
    sys.argv = ['test_script.py']
    script_path = Path(sys.argv[0])
    script_suffix_path = script_path.with_name(f"{script_path.stem}-script.py")
    script_suffix_path.touch()

    args = get_child_arguments()
    assert args[0] == sys.executable
    assert args[1] == script_suffix_path
    assert args[2:] == sys.argv[1:]

    # Cleanup
    script_suffix_path.unlink()

def test_get_child_arguments_raises_runtimeerror_when_script_not_exist():
    sys.argv = ['non_existing_script.py']
    with pytest.raises(RuntimeError, match='Script non_existing_script.py does not exist.'):
        get_child_arguments()