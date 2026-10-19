import os
import pytest
from django.core.management import Command
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.apps import apps

@pytest.fixture
def setup_settings():
    settings.FIXTURE_DIRS = ['/path/to/fixtures']
    yield
    settings.FIXTURE_DIRS = []

def test_fixture_dirs_no_duplicates(setup_settings):
    command = Command()
    command.app_label = None
    
    app_config = apps.get_app_config('auth')
    app_fixtures_dir = os.path.join(app_config.path, "fixtures")
    
    # Simulate the existence of the fixtures directory
    os.makedirs(app_fixtures_dir, exist_ok=True)
    
    expected_dirs = [os.path.realpath(app_fixtures_dir), 
                     os.path.realpath('/path/to/fixtures'), 
                     os.path.realpath('')]
    fixture_dirs = command.fixture_dirs()
    
    assert sorted(fixture_dirs) == sorted(expected_dirs)

def test_fixture_dirs_with_duplicates(setup_settings):
    settings.FIXTURE_DIRS = ['/path/to/fixtures', '/path/to/fixtures']
    command = Command()
    
    with pytest.raises(ImproperlyConfigured, match="settings.FIXTURE_DIRS contains duplicates."):
        command.fixture_dirs()

def test_fixture_dirs_app_default_directory(setup_settings):
    command = Command()
    
    app_config = apps.get_app_config('auth')
    app_fixtures_dir = os.path.join(app_config.path, "fixtures")
    
    # Prevent conflicts by removing the directories if they exist
    if os.path.exists(app_fixtures_dir):
        os.rmdir(app_fixtures_dir)
    
    settings.FIXTURE_DIRS = [app_fixtures_dir]
    
    with pytest.raises(ImproperlyConfigured, match="'%s' is a default fixture directory for the '%s' app" % (app_fixtures_dir, 'auth')):
        command.fixture_dirs()