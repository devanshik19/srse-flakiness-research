import sys
import os
import pytest
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments(mocker):
    # Mock `__main__` for different scenarios.
    mock_main = mocker.patch('builtins.__main__')
    mock_main.__spec__ = None  # No __spec__
    
    # Test case: Script file exists
    mocker.patch('django.utils.autoreload.Path.exists', return_value=True)
    mocker.patch('sys.argv', ['script.py', '--arg1', 'value1'])
    
    # Expected args for the case where script exists
    expected_args = ['python', '-Wignore', 'script.py', '--arg1', 'value1']
    result = get_child_arguments()
    
    assert result == expected_args

    # Test case: Script file does not exist but .exe version does
    mock_main.__spec__ = mocker.Mock(parent='parent_module')
    mocker.patch('django.utils.autoreload.Path.exists', side_effect=lambda: False)
    mocker.patch('django.utils.autoreload.Path.with_suffix', return_value=Path('script.exe'))
    mocker.patch('django.utils.autoreload.Path.with_name', return_value=Path('script-script.py'))
    
    # Mocking that the .exe file exists
    mocker.patch('django.utils.autoreload.Path.exists', side_effect=lambda: True)
    sys.executable = 'python'  # Simulating the executable location
    result = get_child_arguments()
    
    assert result == ['script.exe', '--arg1', 'value1']

    # Test case: Neither script nor .exe exists
    mocker.patch('django.utils.autoreload.Path.exists', side_effect=lambda: False)
    
    with pytest.raises(RuntimeError, match='Script .* does not exist.'):
        get_child_arguments()

    # Test case: Script exists with suffix handling
    mocker.patch('django.utils.autoreload.Path.exists', return_value=False)
    mocker.patch('django.utils.autoreload.Path.with_suffix', side_effect=lambda s: Path('script' + s))
    
    # Mock that script-script.py exists
    mocker.patch('django.utils.autoreload.Path.with_name', return_value=Path('script-script.py'))
    mocker.patch('django.utils.autoreload.Path.exists', side_effect=lambda: True)

    result = get_child_arguments()
    assert result == ['python', '-Wignore', 'script-script.py', '--arg1', 'value1']