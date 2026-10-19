import os
import pytest
from pathlib import Path
from django.template import engines
from django.template.backends.django import DjangoTemplates
from django.utils._os import to_path
from django.utils.autoreload import is_django_path

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

@pytest.mark.parametrize("template_dirs, expected_dirs", [
    (['/templates', '/other_templates'], {Path.cwd() / 'templates', Path.cwd() / 'other_templates'}),
    (['/ignored_template'], set())  # Simulate no valid template directories
])
def test_get_template_directories(monkeypatch, template_dirs, expected_dirs):
    class MockEngine:
        def __init__(self, dirs):
            self.dirs = dirs
            self.template_loaders = []

    class MockLoader:
        def get_dirs(self):
            return ['/valid_template']

    # Create mock engines to return from engines.all()
    monkeypatch.setattr(engines, 'all', lambda: [MockEngine(template_dirs)])

    # Patch is_django_path to return False
    monkeypatch.setattr('django.utils.autoreload.is_django_path', lambda path: path.startswith('/ignored'))

    # Add mock loader
    mock_engine = MockEngine(template_dirs)
    mock_engine.template_loaders.append(MockLoader())
    monkeypatch.setattr(engines, 'all', lambda: [mock_engine])

    result = get_template_directories()

    assert result == expected_dirs.union({Path.cwd() / 'valid_template'})