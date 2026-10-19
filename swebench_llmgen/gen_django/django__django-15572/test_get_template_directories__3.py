import pytest
from pathlib import Path
from django.template import engines
from django.template.backends.django import DjangoTemplates
from django.utils._os import to_path
from django.utils.autoreload import is_django_path

from django.contrib.auth.models import User
from django.conf import settings

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
    # Set up the template directories in the settings
    test_template_dir = Path(__file__).resolve().parent / "test_templates"
    settings.TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [str(test_template_dir)],
            'OPTIONS': {
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ],
            },
        },
    ]

    # Create a test directory and files for template loading
    test_template_dir.mkdir(exist_ok=True)
    (test_template_dir / 'index.html').write_text('Test Template')

    result = get_template_directories()

    # Check if the result contains the test template directory
    assert (Path.cwd() / test_template_dir).resolve() in result

    # Clean up the created test template directory
    for template_file in test_template_dir.iterdir():
        template_file.unlink()
    test_template_dir.rmdir()