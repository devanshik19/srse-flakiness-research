import os
import pytest
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User

@pytest.fixture
def setup_fixture_dirs(monkeypatch):
    # Set up a dummy fixture directory within the app's path
    app_config = apps.get_app_config("auth")
    app_fixtures_path = os.path.join(app_config.path, "fixtures")
    
    # Create the fixtures directory for testing
    os.makedirs(app_fixtures_path, exist_ok=True)
    
    # Set the TESTING setting and FIXTURE_DIRS
    settings.FIXTURE_DIRS = [app_fixtures_path, "/mock/dir"]
    yield
    # Clean up after the test
    if os.path.exists(app_fixtures_path):
        os.rmdir(app_fixtures_path)

def test_fixture_dirs_with_existing_fixtures(setup_fixture_dirs):
    command = Command()
    result = command.fixture_dirs()
    
    app_config = apps.get_app_config("auth")
    expected_dir = os.path.realpath(os.path.join(app_config.path, "fixtures"))
    assert expected_dir in result
    assert "/mock/dir" in result
    assert "" in result

def test_fixture_dirs_with_duplicates(setup_fixture_dirs, monkeypatch):
    monkeypatch.setattr(settings, "FIXTURE_DIRS", ["/mock/dir", "/mock/dir"])
    command = Command()
    
    with pytest.raises(ImproperlyConfigured, match="contains duplicates"):
        command.fixture_dirs()

def test_fixture_dirs_with_default_app_fixture_dir(setup_fixture_dirs, monkeypatch):
    app_config = apps.get_app_config("auth")
    default_fixture_dir = os.path.join(app_config.path, "fixtures")
    
    monkeypatch.setattr(settings, "FIXTURE_DIRS", [default_fixture_dir])
    command = Command()
    
    with pytest.raises(ImproperlyConfigured, match=f"'{default_fixture_dir}' is a default fixture directory for the 'auth' app"):
        command.fixture_dirs()