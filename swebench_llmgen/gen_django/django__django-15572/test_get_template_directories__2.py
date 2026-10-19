import pytest
from pathlib import Path
from django.template import engines
from django.template.backends.django import DjangoTemplates
from django.utils._os import to_path
from django.utils.autoreload import is_django_path
from django.contrib.auth.models import User

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
    # Set up a template dir in settings to be recognized by Django's template engine
    settings.TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    # Creating a temporary directory for testing
    cwd = Path.cwd()
    temp_dir = cwd / 'templates'
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Simulate a template loader that returns a directory
    class TestLoader:
        def get_dirs(self):
            return ['extra_templates']

    # Add the TestLoader to the backend
    backend = engines['django']
    backend.engine.template_loaders.append(TestLoader())

    # Run the focal function
    directories = get_template_directories()

    # Check if the results contain expected template directories
    assert temp_dir in directories
    assert (cwd / to_path('extra_templates')) in directories

    # Clean up
    temp_dir.rmdir()