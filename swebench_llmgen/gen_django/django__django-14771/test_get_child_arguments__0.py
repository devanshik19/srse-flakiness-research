import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

@pytest.fixture
def setup_script(mocker):
    mocker.patch('sys.argv', ['test_script.py', 'arg1', 'arg2'])
    mocker.patch('sys.executable', 'python3')
    mocker.patch('pathlib.Path.exists', return_value=True)

def test_get_child_arguments_existing_script(setup_script):
    with patch('django.utils.autoreload.__main__', new_callable=MagicMock) as mock_main:
        mock_spec = MagicMock()
        mock_spec.name = '__main__'
        mock_spec.parent = None
        mock_main.__spec__ = mock_spec
        
        result = get_child_arguments()
        assert result == ['python3', '-Wnone', 'arg1', 'arg2']

def test_get_child_arguments_existing_module(setup_script):
    with patch('django.utils.autoreload.__main__', new_callable=MagicMock) as mock_main:
        mock_spec = MagicMock()
        mock_spec.name = 'some_module.__main__'
        mock_spec.parent = 'some_module'
        mock_main.__spec__ = mock_spec
        
        result = get_child_arguments()
        assert result == ['python3', '-Wnone', '-m', 'some_module', 'arg1', 'arg2']

def test_get_child_arguments_exe_not_exist(setup_script):
    with patch('django.utils.autoreload.__main__', new_callable=MagicMock) as mock_main:
        mock_main.__spec__ = None
        mock_path = mocker.patch('pathlib.Path.exists', side_effect=lambda: False)

        result = get_child_arguments()
        assert result == ['python3', '-Wnone', 'test_script.py', 'arg1', 'arg2']

def test_get_child_arguments_valid_exe(setup_script):
    with patch('django.utils.autoreload.__main__', new_callable=MagicMock) as mock_main:
        mocker.patch('pathlib.Path.with_suffix', return_value=Path('test_script.exe'))
        mocker.patch('pathlib.Path.exists', side_effect=lambda: True)

        result = get_child_arguments()
        assert result == ['test_script.exe', 'arg1', 'arg2']

def test_get_child_arguments_script_not_exist(setup_script):
    with patch('django.utils.autoreload.__main__', new_callable=MagicMock) as mock_main:
        mock_main.__spec__ = None
        mock_path = mocker.patch('pathlib.Path.exists', side_effect=lambda: False)

        with pytest.raises(RuntimeError, match='Script .* does not exist.'):
            get_child_arguments()