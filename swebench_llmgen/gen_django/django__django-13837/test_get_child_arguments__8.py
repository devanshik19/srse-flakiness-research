import sys
import pytest
import django
from pathlib import Path
from django.contrib.auth.models import User

def test_get_child_arguments_when_running_django_main():
    sys.argv = [str(Path(django.__main__.__file__)), 'runserver']
    expected_args = [sys.executable, '-W{}'.format(o) for o in sys.warnoptions] + ['-m', 'django', 'runserver']
    
    result = get_child_arguments()
    
    assert result == expected_args

def test_get_child_arguments_when_py_script_does_not_exist():
    py_script = Path(sys.argv[0]).with_name('non_existent_script.py')
    sys.argv = [str(py_script)]
    
    exe_entrypoint = py_script.with_suffix('.exe')
    script_entrypoint = py_script.with_name(f'{py_script.name}-script.py')
    
    # Mocking the behavior of path exists
    exists_original = Path.exists
    def mock_exists(self):
        return self in {exe_entrypoint, script_entrypoint}
    
    Path.exists = mock_exists
    
    result = get_child_arguments()
    
    assert result == [str(script_entrypoint), *sys.argv[1:]]
    
    Path.exists = exists_original

def test_get_child_arguments_when_script_exists_as_exe():
    py_script = Path(sys.argv[0]).with_name('test_script.py')
    exe_entrypoint = py_script.with_suffix('.exe')
    
    sys.argv = [str(py_script)]
    
    # Mocking the behavior of path exists
    exists_original = Path.exists
    def mock_exists(self):
        return self == exe_entrypoint

    Path.exists = mock_exists

    result = get_child_arguments()

    assert result == [str(exe_entrypoint), *sys.argv[1:]]

    Path.exists = exists_original

def test_get_child_arguments_when_script_exists_as_script():
    py_script = Path(sys.argv[0]).with_name('test_script.py')
    script_entrypoint = py_script.with_name(f'{py_script.stem}-script.py')
    
    sys.argv = [str(py_script)]
    
    # Mocking the behavior of path exists
    exists_original = Path.exists
    def mock_exists(self):
        return self == script_entrypoint

    Path.exists = mock_exists

    result = get_child_arguments()

    assert result == [sys.executable] + ['-W{}'.format(o) for o in sys.warnoptions] + [str(script_entrypoint), *sys.argv[1:]]

    Path.exists = exists_original

def test_get_child_arguments_when_script_does_not_exist_raises_runtime_error():
    py_script = Path(sys.argv[0]).with_name('non_existent_script.py')
    sys.argv = [str(py_script)]
    
    with pytest.raises(RuntimeError, match='Script non_existent_script.py does not exist.'):
        get_child_arguments()