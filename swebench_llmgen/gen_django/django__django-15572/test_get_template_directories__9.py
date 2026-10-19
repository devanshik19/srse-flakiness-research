import pytest
from pathlib import Path
from django.template import engines
from django.template.backends.django import DjangoTemplates
from django.utils._os import to_path
from django.utils.autoreload import autoreload_started, file_changed, is_django_path

# Assume a test template loader for demonstration purposes
class TestLoader:
    def get_dirs(self):
        return ['template_dir_1', 'template_dir_2']

# Mocking DjangoTemplates engine for testing
class MockDjangoTemplates(DjangoTemplates):
    def __init__(self):
        self.engine = type('Engine', (), {
            'dirs': ['template_dir_1', 'template_dir_2'],
            'template_loaders': [TestLoader()]
        })()
        super().__init__()

engines.unregister('django.template.backends.django.DjangoTemplates')
engines.register('django.template.backends.django.DjangoTemplates', MockDjangoTemplates)

from django.template.autoreload import get_template_directories

def test_get_template_directories(monkeypatch):
    cwd = Path.cwd()
    expected_dirs = {
        cwd / to_path('template_dir_1'),
        cwd / to_path('template_dir_2'),
        cwd / to_path('template_dir_1'),
        cwd / to_path('template_dir_2'),
    }
    
    result = get_template_directories()
    
    assert result == expected_dirs