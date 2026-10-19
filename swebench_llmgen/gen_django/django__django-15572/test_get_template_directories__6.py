import pytest
from django.template import engines
from django.template.backends.django import DjangoTemplates
from django.utils._os import to_path
from django.utils.autoreload import is_django_path
from pathlib import Path

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

def test_get_template_directories(monkeypatch):
    # Prepare test template backends
    class FakeLoader:
        def get_dirs(self):
            return ["my_templates", "another_dir"]

    class FakeBackend:
        engine = type("Engine", (), {"dirs": ["dir1", "dir2"], "template_loaders": [FakeLoader()]})

    monkeypatch.setattr(engines, 'all', lambda: [FakeBackend(), DjangoTemplates()])

    expected_dirs = {
        Path.cwd() / "dir1",
        Path.cwd() / "dir2",
        Path.cwd() / "my_templates",
        Path.cwd() / "another_dir"
    }

    result = get_template_directories()

    assert result == expected_dirs