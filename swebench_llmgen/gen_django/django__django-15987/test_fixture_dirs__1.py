import os
import pytest
from django.core.management import CommandError
from django.conf import settings
from django.apps import apps
from django.contrib.auth.models import User

@pytest.fixture
def setup_fixture_dirs(settings):
    settings.FIXTURE_DIRS = [os.path.join(os.getcwd(), 'fixtures')]
    yield
    settings.FIXTURE_DIRS = []

def test_fixture_dirs_no_duplicates(setup_fixture_dirs):
    command = Command()
    app_config = apps.get_app_config('auth')  # Using 'auth' as a sample app
    os.makedirs(os.path.join(app_config.path, 'fixtures'), exist_ok=True)
    
    dirs = command.fixture_dirs()
    
    assert os.path.realpath(os.path.join(app_config.path, 'fixtures')) in dirs
    assert os.path.realpath(settings.FIXTURE_DIRS[0]) in dirs
    assert "" in dirs

def test_fixture_dirs_with_duplicates(setup_fixture_dirs):
    command = Command()
    settings.FIXTURE_DIRS = [os.path.join(os.getcwd(), 'fixtures')] * 2
    with pytest.raises(CommandError):
        command.fixture_dirs()

def test_fixture_dirs_default_directory(setup_fixture_dirs):
    command = Command()
    app_config = apps.get_app_config('auth')  # Using 'auth' as a sample app
    app_dir = os.path.join(app_config.path, 'fixtures')
    os.makedirs(app_dir, exist_ok=True)
    
    # directory should not be included if it is in FIXTURE_DIRS
    settings.FIXTURE_DIRS = [app_dir]
    
    with pytest.raises(CommandError):
        command.fixture_dirs()
    
def test_fixture_dirs_empty_directory(setup_fixture_dirs):
    command = Command()
    # Testing with no app directories or fixture directories
    dirs = command.fixture_dirs()
    
    assert dirs == ['']  # Only the empty string should be returned