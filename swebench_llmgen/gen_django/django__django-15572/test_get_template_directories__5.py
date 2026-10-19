import pytest
from django.template import engines
from django.template.backends.django import DjangoTemplates
from django.utils._os import to_path
from django.utils.autoreload import is_django_path
from pathlib import Path

# Import the focal function
from django.template.autoreload import get_template_directories

@pytest.fixture
def setup_template_engines(settings):
    settings.TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['/template/dir1', '/template/dir2'],
            'APP_DIRS': True,
        },
        {
            'BACKEND': 'another.backend.NonDjangoTemplates',
            'DIRS': ['/other/dir'],
        },
    ]
    
    yield

def test_get_template_directories(setup_template_engines):
    # Patch the `engines.all()` to return a mocked DjangoTemplates backend.
    django_templates_backend = DjangoTemplates({
        'DIRS': ['/template/dir1', '/template/dir2'],
        'APP_DIRS': True,
    })
    engines._template_engines = [django_templates_backend]

    # Test the function
    results = get_template_directories()
    
    # Check results against expected output
    expected_directories = {
        Path.cwd() / to_path('/template/dir1'),
        Path.cwd() / to_path('/template/dir2')
    }
    
    assert results == expected_directories