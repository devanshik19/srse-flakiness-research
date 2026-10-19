import pytest
import sys
from unittest import mock
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_valid_script():
    # Prepare a mock for sys.argv
    sys.argv = ['script.py', 'arg1', 'arg2']
    with mock.patch('django.utils.autoreload.Path.exists', return_value=True):
        args = get_child_arguments()
        assert args == ['python', '-W', '', 'script.py', 'arg1', 'arg2']

def test_get_child_arguments_no_script_exists():
    # Prepare a mock for sys.argv
    sys.argv = ['missing_script.py', 'arg1', 'arg2']
    mock_path = mock.Mock()
    mock_path.exists.side_effect = [False, False]
    
    with mock.patch('django.utils.autoreload.Path.exists', mock_path.exists):
        with mock.patch('django.utils.autoreload.Path.with_suffix', return_value=mock_path):
            with mock.patch('django.utils.autoreload.Path.with_name', return_value=mock_path):
                with pytest.raises(RuntimeError, match='Script missing_script.py does not exist.'):
                    get_child_arguments()

def test_get_child_arguments_exe_entrypoint_exists():
    # Prepare a mock for sys.argv
    sys.argv = ['script.py', 'arg1', 'arg2']
    mock_path = mock.Mock()
    mock_path.exists.side_effect = [True, False]
    
    with mock.patch('django.utils.autoreload.Path.exists', mock_path.exists):
        with mock.patch('django.utils.autoreload.Path.with_suffix', return_value=mock_path):
            args = get_child_arguments()
            assert args == [mock_path, 'arg1', 'arg2']

def test_get_child_arguments_script_entrypoint_exists():
    # Prepare a mock for sys.argv
    sys.argv = ['script.py', 'arg1', 'arg2']
    mock_path = mock.Mock()
    mock_path.exists.side_effect = [False, True]
    
    with mock.patch('django.utils.autoreload.Path.exists', mock_path.exists):
        with mock.patch('django.utils.autoreload.Path.with_suffix', return_value=mock_path):
            with mock.patch('django.utils.autoreload.Path.with_name', return_value=mock_path):
                args = get_child_arguments()
                assert args == ['python', '-W', '', mock_path, 'arg1', 'arg2']