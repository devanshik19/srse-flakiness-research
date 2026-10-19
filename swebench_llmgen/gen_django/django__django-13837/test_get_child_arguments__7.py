import sys
import pytest
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments
from unittest.mock import patch, MagicMock
from pathlib import Path

@pytest.fixture
def mock_django_main_file(tmp_path):
    django_main = tmp_path / 'django' / '__main__.py'
    django_main.parent.mkdir(parents=True, exist_ok=True)
    django_main.write_text("# Django main module")
    return str(django_main)

def test_get_child_arguments_runserver(mock_django_main_file):
    with patch('django.__main__.__file__', mock_django_main_file):
        sys.argv = ['manage.py', 'runserver']
        args = get_child_arguments()
        assert args == [sys.executable, '-W%s' % o for o in sys.warnoptions] + ['-m', 'django', 'runserver']

def test_get_child_arguments_executable(mock_django_main_file):
    with patch('django.__main__.__file__', mock_django_main_file):
        sys.argv = ['my_script', 'arg1', 'arg2']
        mock_script = Path('my_script')
        mock_script.write_text("print('Sample script')")
        assert mock_script.exists()
        
        # Simulating the existence of exe and script.py suffixes
        exe_script = mock_script.with_suffix('.exe')
        script_py = mock_script.with_name('my_script-script.py')
        
        exe_script.touch()
        script_py.touch()

        args = get_child_arguments()
        assert exe_script.exists()
        assert args == [str(exe_script), 'arg1', 'arg2']

        exe_script.unlink()
        args = get_child_arguments()
        assert args == [str(script_py), 'arg1', 'arg2']

def test_get_child_arguments_non_existing(mock_django_main_file):
    with patch('django.__main__.__file__', mock_django_main_file):
        sys.argv = ['non_existing_script']
        with pytest.raises(RuntimeError) as excinfo:
            get_child_arguments()
        assert 'Script non_existing_script does not exist.' in str(excinfo.value)