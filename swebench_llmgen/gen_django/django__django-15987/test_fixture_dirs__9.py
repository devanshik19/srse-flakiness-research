import os
import pytest
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.commands.loaddata import Command

@pytest.fixture
def command():
    return Command()

def test_fixture_dirs_no_duplicates(command):
    settings.FIXTURE_DIRS = []
    assert command.fixture_dirs() == ['']

def test_fixture_dirs_with_fixtures(command):
    app_config = apps.get_app_config('auth')
    app_dir = os.path.join(app_config.path, 'fixtures')
    os.makedirs(app_dir, exist_ok=True)

    settings.FIXTURE_DIRS = []
    assert command.fixture_dirs() == [os.path.realpath(app_dir), '', ]

def test_fixture_dirs_with_invalid_fixture_dir(command):
    app_config = apps.get_app_config('auth')
    app_dir = os.path.join(app_config.path, 'fixtures')
    os.makedirs(app_dir, exist_ok=True)

    settings.FIXTURE_DIRS = [app_dir]  # This should raise an error
    with pytest.raises(ImproperlyConfigured):
        command.fixture_dirs()

def test_fixture_dirs_with_non_existing_directory(command):
    settings.FIXTURE_DIRS = ['/non/existing/dir']
    result = command.fixture_dirs()
    assert '/non/existing/dir' in result
    assert '' in result

def test_fixture_dirs_with_duplicates(command):
    settings.FIXTURE_DIRS = ['my_fixture_dir', 'my_fixture_dir']
    with pytest.raises(ImproperlyConfigured):
        command.fixture_dirs()

def test_fixture_dirs_with_app_specific(command):
    app_config = apps.get_app_config('auth')
    app_dir = os.path.join(app_config.path, 'fixtures')
    os.makedirs(app_dir, exist_ok=True)

    settings.FIXTURE_DIRS = ['/another/fixture/dir']
    result = command.fixture_dirs()
    assert app_dir in result
    assert '/another/fixture/dir' in result
    assert '' in result