import os
import pytest
from django.conf import settings
from django.core.management import Command
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock

@pytest.fixture
def set_fixture_dirs():
    original_fixture_dirs = settings.FIXTURE_DIRS
    settings.FIXTURE_DIRS = ['custom_fixtures']
    yield
    settings.FIXTURE_DIRS = original_fixture_dirs

def test_fixture_dirs_no_duplicates(set_fixture_dirs):
    command = Command()
    with patch('django.apps.apps.get_app_configs', return_value=[MagicMock(label='auth', path='/fake/path/auth')]):
        os.makedirs('/fake/path/auth/fixtures', exist_ok=True)
        dirs = command.fixture_dirs()
        assert '/fake/path/auth/fixtures' in dirs
        assert 'custom_fixtures' in dirs
        assert '' in dirs

def test_fixture_dirs_with_duplicates(set_fixture_dirs):
    settings.FIXTURE_DIRS = ['duplicate_fixtures', 'duplicate_fixtures']
    command = Command()
    with pytest.raises(ImproperlyConfigured, match="settings.FIXTURE_DIRS contains duplicates."):
        command.fixture_dirs()

def test_fixture_dirs_app_default_conflict(set_fixture_dirs):
    command = Command()
    with patch('django.apps.apps.get_app_configs', return_value=[MagicMock(label='auth', path='/fake/path/auth')]):
        os.makedirs('/fake/path/auth/fixtures', exist_ok=True)
        settings.FIXTURE_DIRS = ['/fake/path/auth/fixtures']
        with pytest.raises(ImproperlyConfigured, match="'/fake/path/auth/fixtures' is a default fixture directory for the 'auth' app"):
            command.fixture_dirs()