import os
import pytest
from django.core.management import Command
from django.conf import settings
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User

# Setting up test settings
@pytest.fixture(autouse=True)
def set_test_settings(monkeypatch):
    monkeypatch.setattr(settings, 'FIXTURE_DIRS', [])
    monkeypatch.setattr(settings, 'INSTALLED_APPS', ['django.contrib.auth'])

def test_fixture_dirs_no_duplicates():
    command = Command()
    result = command.fixture_dirs()
    assert result == ['', '/path/to/fixtures']  # Adjust based on expected output.

def test_fixture_dirs_with_fixture_dirs():
    command = Command()
    monkeypatch.setattr(settings, 'FIXTURE_DIRS', ['/my/custom/fixtures'])
    result = command.fixture_dirs()
    assert result == ['/path/to/fixtures', '/my/custom/fixtures', '']  # Adjust as necessary.

def test_fixture_dirs_with_duplicate_fixture_dirs():
    command = Command()
    monkeypatch.setattr(settings, 'FIXTURE_DIRS', ['/my/custom/fixtures', '/my/custom/fixtures'])
    with pytest.raises(ImproperlyConfigured):
        command.fixture_dirs()

def test_fixture_dirs_with_app_fixtures(monkeypatch):
    apps.get_app_configs = lambda: [type('AppConfig', (object,), {'label': 'auth', 'path': '/path/to'})]
    monkeypatch.setattr(settings, 'FIXTURE_DIRS', ['/my/custom/fixtures'])
    command = Command()
    result = command.fixture_dirs()
    assert result == ['/path/to/fixtures', '/my/custom/fixtures', '']  # Adjust as necessary.

def test_fixture_dirs_excludes_default_fixtures():
    apps.get_app_configs = lambda: [type('AppConfig', (object,), {'label': 'auth', 'path': '/path/to'})]
    monkeypatch.setattr(settings, 'FIXTURE_DIRS', ['/path/to/fixtures'])
    command = Command()
    with pytest.raises(ImproperlyConfigured):
        command.fixture_dirs()