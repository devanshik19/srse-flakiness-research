import os
import pytest
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.core.management.commands.loaddata import Command

@pytest.fixture
def configure_settings():
    settings.FIXTURE_DIRS = ['/valid/fixture/dir']
    yield
    settings.FIXTURE_DIRS = []

def test_fixture_dirs_empty(configure_settings):
    command = Command()
    command.app_label = None
    result = command.fixture_dirs()
    assert result == ['/valid/fixture/dir', '']

def test_fixture_dirs_with_app_fixtures(configure_settings):
    app_config = apps.get_appConfig('auth')
    os.makedirs(os.path.join(app_config.path, 'fixtures'), exist_ok=True)
    command = Command()
    command.app_label = None
    result = command.fixture_dirs()
    assert os.path.realpath(result[0]) == os.path.realpath(os.path.join(app_config.path, 'fixtures'))
    assert '/valid/fixture/dir' in result
    assert '' in result

def test_fixture_dirs_with_duplicates(configure_settings):
    settings.FIXTURE_DIRS = ['/valid/fixture/dir', '/valid/fixture/dir']
    command = Command()
    command.app_label = None
    with pytest.raises(ImproperlyConfigured, match="settings.FIXTURE_DIRS contains duplicates."):
        command.fixture_dirs()

def test_fixture_dirs_app_default_in_fixture_dirs(configure_settings):
    app_config = apps.get_appConfig('auth')
    app_dir = os.path.join(app_config.path, 'fixtures')
    settings.FIXTURE_DIRS = [app_dir]
    command = Command()
    command.app_label = None
    with pytest.raises(ImproperlyConfigured, match=f"'%s' is a default fixture directory for the '%s' app" % (app_dir, app_config.label)):
        command.fixture_dirs()

def test_fixture_dirs_with_app_label(configure_settings):
    app_config = apps.get_appConfig('auth')
    os.makedirs(os.path.join(app_config.path, 'fixtures'), exist_ok=True)
    command = Command()
    command.app_label = 'auth'
    result = command.fixture_dirs()
    assert os.path.realpath(result[0]) == os.path.realpath(os.path.join(app_config.path, 'fixtures'))
    assert len(result) == 2  # Only includes the specific app directory and ''