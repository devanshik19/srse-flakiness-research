import os
import sys
import pytest
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments_with_runserver():
    # Simulate the command to launch Django runserver
    sys.argv = ['manage.py', 'runserver']
    result = get_child_arguments()

    # Check that the output is correct
    assert result[0] == sys.executable
    assert result[1] == '-W' + str(os.environ.get('PYTHONWARNINGS', 'default'))
    assert result[2] == '-m'
    assert result[3] == 'django'
    assert result[4] == 'runserver'

def test_get_child_arguments_with_script_existence(mocker):
    # Simulate a script existing on the path
    mocker.patch('django.__main__.__file__', new='manage.py')
    
    # Create fake script file for test
    script_path = 'manage-script.py'
    with open(script_path, 'w') as f:
        f.write('# Fake script file for testing')

    sys.argv = ['manage.py']
    result = get_child_arguments()

    # Check that the output correctly references the script
    assert result[-1] == 'manage-script.py'
    
    # Cleanup
    os.remove(script_path)

def test_get_child_arguments_with_exe_existence(mocker):
    # Simulate the script path scenario for .exe
    mocker.patch('django.__main__.__file__', new='manage.py')
    
    # Create fake executable file for test
    exe_path = 'manage.exe'
    with open(exe_path, 'w') as f:
        f.write('# Fake executable file for testing')

    sys.argv = ['manage.py']
    result = get_child_arguments()

    # Check that the executable output is correct
    assert result[0] == exe_path
    
    # Cleanup
    os.remove(exe_path)

def test_get_child_arguments_with_nonexistent_script():
    sys.argv = ['nonexistent_script.py']
    with pytest.raises(RuntimeError, match='Script nonexistent_script.py does not exist.'):
        get_child_arguments()