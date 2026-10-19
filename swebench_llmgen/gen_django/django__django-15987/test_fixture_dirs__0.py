import os
import pytest
from django.conf import settings
from django.core.management import CommandError
from django.apps import apps
from django.contrib.auth.models import User

class TestCommand:

    @pytest.fixture(autouse=True)
    def setup_fixtures(self, settings, monkeypatch):
        # Ensure settings.FIXTURE_DIRS is set
        settings.FIXTURE_DIRS = []
        # Create a sample app with a fixtures directory
        app_name = 'testapp'
        os.makedirs(os.path.join(os.getcwd(), app_name, 'fixtures'), exist_ok=True)
        monkeypatch.setattr(apps, 'get_app_configs', lambda: [apps.get_app_config(app_name)])
        monkeypatch.setattr('django.conf.settings.INSTALLED_APPS', [app_name])

    def test_fixture_dirs_with_default_fixtures(self):
        cmd = Command()
        result = cmd.fixture_dirs()
        assert os.path.realpath(os.path.join(os.getcwd(), 'testapp', 'fixtures')) in result
        assert "" in result
        assert settings.FIXTURE_DIRS == result[1:]  # The first item should be the app's fixtures dir

    def test_fixture_dirs_with_custom_fixture_dirs(self, monkeypatch):
        custom_dir = '/custom/fixtures'
        settings.FIXTURE_DIRS = [custom_dir]
        cmd = Command()
        result = cmd.fixture_dirs()
        assert custom_dir in result
        assert os.path.realpath(os.path.join(os.getcwd(), 'testapp', 'fixtures')) in result

    def test_fixture_dirs_with_duplicate_entries(self, monkeypatch):
        settings.FIXTURE_DIRS = ['dir1', 'dir2', 'dir1']  # duplicate
        cmd = Command()
        with pytest.raises(CommandError, match="settings.FIXTURE_DIRS contains duplicates."):
            cmd.fixture_dirs()

    def test_fixture_dirs_default_app_dir_in_fixture_dirs(self, monkeypatch):
        app_dir = os.path.join(os.getcwd(), 'testapp', 'fixtures')
        settings.FIXTURE_DIRS = [app_dir]  # should raise an error
        cmd = Command()
        with pytest.raises(CommandError, match=f"'{app_dir}' is a default fixture directory for the 'testapp' app"):
            cmd.fixture_dirs()