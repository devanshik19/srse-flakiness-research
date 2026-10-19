import pytest
from django.contrib.auth.models import User
from django.template import engines
from django.template.backends.django import DjangoTemplates
from django.utils._os import to_path
from django.utils.autoreload import autoreload_started, file_changed, is_django_path
from pathlib import Path

from django.template.autoreload import get_template_directories

@pytest.fixture
def setup_templates(settings):
    # Setup template directories for testing
    settings.TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['my_template_dir1', 'my_template_dir2'],
            'APP_DIRS': True,
            'OPTIONS': {
                'loaders': [
                    ('django.template.loaders.filesystem.Loader',),
                    ('django.template.loaders.app_directories.Loader',),
                ],
            },
        },
    ]

@pytest.mark.usefixtures("setup_templates")
def test_get_template_directories():
    # Create current working directory mock
    cwd = Path.cwd()

    # Call the focal function
    directories = get_template_directories()

    # Validate the output
    assert (cwd / to_path('my_template_dir1')).in_path(directories)
    assert (cwd / to_path('my_template_dir2')).in_path(directories)

    # Also test with DjangoTemplates loaders
    for backend in engines.all():
        if isinstance(backend, DjangoTemplates):
            for loader in backend.engine.template_loaders:
                if hasattr(loader, "get_dirs"):
                    result_dirs = loader.get_dirs()
                    for dir in result_dirs:
                        if not is_django_path(dir):
                            assert (cwd / to_path(dir)).in_path(directories)