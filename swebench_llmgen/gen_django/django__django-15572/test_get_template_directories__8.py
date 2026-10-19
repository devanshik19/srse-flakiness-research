import pytest
from pathlib import Path
from django.template import engines
from django.template.backends.django import DjangoTemplates
from django.utils._os import to_path
from django.utils.autoreload import is_django_path

# Assuming this is part of the same module as get_template_directories
def get_template_directories():
    cwd = Path.cwd()
    items = set()
    for backend in engines.all():
        if not isinstance(backend, DjangoTemplates):
            continue

        items.update(cwd / to_path(dir) for dir in backend.engine.dirs)

        for loader in backend.engine.template_loaders:
            if not hasattr(loader, "get_dirs"):
                continue
            items.update(
                cwd / to_path(directory)
                for directory in loader.get_dirs()
                if not is_django_path(directory)
            )
    return items

# Test cases for the get_template_directories function
def test_get_template_directories(monkeypatch):
    # Setup for the test
    class MockDjangoTemplates:
        def __init__(self, dirs):
            self.dirs = dirs
            self.template_loaders = [MockLoader(dirs)]

    class MockLoader:
        def __init__(self, dirs):
            self._dirs = dirs

        def get_dirs(self):
            return self._dirs

    # Patch the engines.all() method to return our mock backend
    monkeypatch.setattr(engines, 'all', lambda: [MockDjangoTemplates(['/template/dir1', '/template/dir2'])])

    # Call the function
    result = get_template_directories()

    # Assert that the resulting directories contain the expected paths
    expected_directories = {
        Path.cwd() / 'template' / 'dir1',
        Path.cwd() / 'template' / 'dir2',
    }
    assert result == expected_directories

    # Test with an additional loader that has get_dirs and returns an unwanted django path
    monkeypatch.setattr(engines, 'all', lambda: [MockDjangoTemplates(['django/template/dir'])])

    result = get_template_directories()
    
    # Assert to ensure the django path is filtered out
    unexpected_directory = Path.cwd() / 'django' / 'template' / 'dir'
    assert unexpected_directory not in result