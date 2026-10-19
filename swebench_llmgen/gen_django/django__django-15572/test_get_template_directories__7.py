import pytest
from django.template import engines
from django.template.backends.django import DjangoTemplates
from django.utils._os import to_path
from django.utils.autoreload import is_django_path
from django.contrib.auth.models import User
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

def test_get_template_directories(settings):
    # Setup custom template directories in settings for testing
    settings.TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['templates', 'another_template_dir'],
            'APP_DIRS': False,
            'OPTIONS': {
                'loaders': [
                    ('django.template.loaders.filesystem.Loader',),
                ],
            },
        },
    ]

    # Create a mock directory structure
    template_dir_1 = Path.cwd() / 'templates'
    template_dir_2 = Path.cwd() / 'another_template_dir'
    template_dir_1.mkdir(parents=True, exist_ok=True)
    template_dir_2.mkdir(parents=True, exist_ok=True)
    
    # Simulate get_dirs return values for the test
    class MockLoader:
        def get_dirs(self):
            return ['mock_dir_1', 'mock_dir_2']

    # Assign mock loaders to the engine (internals)
    backend = engines['django']
    backend.engine.template_loaders = [MockLoader()]

    result = get_template_directories()
    
    assert Path.cwd() / to_path('templates') in result
    assert Path.cwd() / to_path('another_template_dir') in result
    assert Path.cwd() / to_path('mock_dir_1') in result
    assert Path.cwd() / to_path('mock_dir_2') in result
    assert not any(is_django_path(str(p)) for p in result)

    # Cleanup the mock directories after test
    template_dir_1.rmdir()
    template_dir_2.rmdir()