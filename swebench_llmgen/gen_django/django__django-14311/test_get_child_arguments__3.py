import sys
import pytest
from django.contrib.auth.models import User
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments(monkeypatch):
    # Test case where __spec__ is not None and has a parent
    class MockMain:
        __spec__ = type("spec", (), {"parent": "mock_parent"})

    monkeypatch.setattr("__main__", MockMain)
    monkeypatch.setattr(sys, 'argv', ['script_name', 'arg1', 'arg2'])
    expected_args = [sys.executable, '-W%s' % o for o in sys.warnoptions] + ['-m', 'mock_parent', 'arg1', 'arg2']
    
    assert get_child_arguments() == expected_args

    # Test case where py_script does not exist but exe_entrypoint does exist
    monkeypatch.setattr('__main__.__spec__', None)
    class MockPath:
        def __init__(self, path):
            self.path = path
        
        def exists(self):
            return False
        
        def with_suffix(self, suffix):
            return MockPath(self.path + suffix)

        def with_name(self, name):
            return MockPath(name)

        @property
        def name(self):
            return 'script_name'

    monkeypatch.setattr("sys.argv[0]", "script_name")
    monkeypatch.setattr("pathlib.Path", MockPath)

    # Simulate existing exe entrypoint
    monkeypatch.setattr(MockPath("script_name.exe"), 'exists', lambda self: True)
    assert get_child_arguments() == ['script_name.exe', 'arg1', 'arg2']

    # Test case where script does not exist
    monkeypatch.setattr(MockPath("script_name.exe"), 'exists', lambda self: False)
    monkeypatch.setattr(MockPath("script_name-script.py"), 'exists', lambda self: False)
    with pytest.raises(RuntimeError) as excinfo:
        get_child_arguments()
    assert 'Script script_name does not exist.' in str(excinfo.value)

    # Test case where py_script exists normally.
    monkeypatch.setattr(MockPath("script_name"), 'exists', lambda self: True)

    assert get_child_arguments() == expected_args