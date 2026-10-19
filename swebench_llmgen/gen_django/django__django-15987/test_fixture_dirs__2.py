import os
import pytest
from django.conf import settings
from django.apps import apps
from django.core.management.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.core.management.commands.loaddata import Command

def test_fixture_dirs_without_duplicates(settings):
    # Arrange
    settings.FIXTURE_DIRS = []
    command = Command()

    # Act
    result = command.fixture_dirs()

    # Assert
    assert isinstance(result, list)
    assert result == [""]

def test_fixture_dirs_with_app_fixtures(settings):
    # Arrange
    settings.FIXTURE_DIRS = []
    app_config = apps.get_app_configs()[0]
    app_dir = os.path.join(app_config.path, "fixtures")

    os.makedirs(app_dir)
    with open(os.path.join(app_dir, 'test_fixture.json'), 'w') as f:
        f.write('[]')

    command = Command()

    # Act
    result = command.fixture_dirs()

    # Assert
    assert isinstance(result, list)
    assert app_dir in result
    assert "" in result

def test_fixture_dirs_with_duplicates(settings):
    # Arrange
    settings.FIXTURE_DIRS = ['duplicate_path', 'duplicate_path']
    command = Command()

    # Act & Assert
    with pytest.raises(ImproperlyConfigured, match="settings.FIXTURE_DIRS contains duplicates."):
        command.fixture_dirs()

def test_fixture_dirs_with_invalid_app_fixture(settings):
    # Arrange
    settings.FIXTURE_DIRS = ['invalid_path']
    app_config = apps.get_app_configs()[0]
    app_dir = os.path.join(app_config.path, "fixtures")

    os.makedirs(app_dir)
    with open(os.path.join(app_dir, 'test_fixture.json'), 'w') as f:
        f.write('[]')

    command = Command()
    
    # Act
    result = command.fixture_dirs()

    # Assert
    assert app_dir in result
    assert "invalid_path" in result