import os
import pytest
from django.apps import apps
from django.conf import settings
from django.core.management import CommandError
from django.core.management.commands.loaddata import Command
from django.contrib.auth.models import User

@pytest.fixture
def setup_fixtures(settings):
    settings.FIXTURE_DIRS = []

@pytest.fixture
def command_instance():
    return Command()

def test_fixture_dirs_no_fixtures(command_instance, setup_fixtures):
    assert command_instance.fixture_dirs() == [""]

def test_fixture_dirs_with_app_fixtures(command_instance, setup_fixtures):
    app_config = apps.get_app_config('auth')
    app_dir = os.path.join(app_config.path, "fixtures")
    os.makedirs(app_dir, exist_ok=True)
    
    expected_dirs = [os.path.realpath(app_dir), "", os.path.realpath(".")]
    assert set(command_instance.fixture_dirs()) == set(expected_dirs)

def test_fixture_dirs_with_duplicate_settings(command_instance, setup_fixtures):
    settings.FIXTURE_DIRS = ['fixtures', 'fixtures']
    with pytest.raises(CommandError, match="contains duplicates"):
        command_instance.fixture_dirs()

def test_fixture_dirs_with_default_directory(command_instance, setup_fixtures):
    app_config = apps.get_app_config('auth')
    app_dir = os.path.join(app_config.path, "fixtures")
    os.makedirs(app_dir, exist_ok=True)
    settings.FIXTURE_DIRS = [app_dir]

    with pytest.raises(CommandError, match="cannot be listed in settings.FIXTURE_DIRS"):
        command_instance.fixture_dirs()