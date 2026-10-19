import sys
import pytest
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

@pytest.mark.parametrize("argv, expected_output", [
    (["manage.py", "runserver"], [sys.executable, '-m', 'django', 'runserver']),
    (["manage.py"], [sys.executable, '-m', 'django']),
    (["not_exist_script"], RuntimeError),
])
def test_get_child_arguments(monkeypatch, argv, expected_output):
    monkeypatch.setattr(sys, 'argv', argv)
    monkeypatch.setattr('django.__main__.__file__', 'manage.py')
    
    if expected_output is RuntimeError:
        with pytest.raises(RuntimeError, match='Script not_exist_script does not exist.'):
            get_child_arguments()
    else:
        result = get_child_arguments()
        assert result[:len(expected_output)] == expected_output