import pytest
from pathlib import Path
from django.template import engines
from django.template.backends.django import DjangoTemplates
from django.utils._os import to_path
from django.utils.autoreload import is_django_path

from django.contrib.auth.models import User  # Importing a built-in model

def test_get_template_directories(monkeypatch):
    # Setup for the test
    test_dir = Path('/test/directory')
    monkeypatch.setattr(Path, 'cwd', lambda: test_dir)

    class MockTemplateLoader:
        def get_dirs(self):
            return ['dir1', 'dir2']

    class MockBackend:
        engine = type('Engine', (), {
            'dirs': ['template_dir'],
            'template_loaders': [MockTemplateLoader()]
        })

    monkeypatch.setattr(engines, 'all', lambda: [DjangoTemplates(MockBackend())])

    # Run the function
    result = get_template_directories()

    # Assertions
    expected_dirs = {
        test_dir / to_path('template_dir'), 
        test_dir / to_path('dir1'), 
        test_dir / to_path('dir2')
    }
    
    assert result == expected_dirs
    assert not any(is_django_path(str(directory)) for directory in result)