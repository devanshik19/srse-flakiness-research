import sys
import pytest
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments
from unittest.mock import patch, MagicMock

def test_get_child_arguments_with_module_spec():
    with patch('sys.argv', ['test_script.py', 'arg1', 'arg2']):
        mock_main = MagicMock()
        mock_main.__spec__ = MagicMock(name='spec', wraps=object)
        mock_main.__spec__.name = '__main__'
        mock_main.__spec__.parent = 'test'
        
        with patch('builtins.__import__', return_value=mock_main):
            args = get_child_arguments()
            assert args == ['python', '-W', 'default', '-m', 'test_script', 'arg1', 'arg2']

def test_get_child_arguments_with_nonexistent_script():
    with patch('sys.argv', ['non_existent_script.py']):
        with patch('pathlib.Path.exists', return_value=False):
            with pytest.raises(RuntimeError, match='Script non_existent_script.py does not exist.'):
                get_child_arguments()

def test_get_child_arguments_with_executable_suffix():
    with patch('sys.argv', ['test_script']):
        mock_path = MagicMock()
        mock_path.with_suffix.return_value.exists.return_value = True
        with patch('pathlib.Path', return_value=mock_path):
            args = get_child_arguments()
            assert args == [mock_path.with_suffix.return_value, '']

def test_get_child_arguments_with_script_suffix():
    with patch('sys.argv', ['test_script']):
        mock_path = MagicMock()
        mock_path.with_suffix.return_value.exists.return_value = False
        mock_path.with_name.return_value.exists.return_value = True
        with patch('pathlib.Path', return_value=mock_path):
            args = get_child_arguments()
            assert args == ['python', '-W', 'default', mock_path.with_name.return_value, '']

def test_get_child_arguments_default_case():
    with patch('sys.argv', ['test_script.py', 'arg1', 'arg2']):
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        with patch('pathlib.Path', return_value=mock_path):
            args = get_child_arguments()
            assert args == ['python', '-W', 'default', 'test_script.py', 'arg1', 'arg2']