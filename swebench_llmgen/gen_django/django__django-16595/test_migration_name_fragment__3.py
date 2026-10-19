import pytest
from django.db.migrations.operations.fields import AddField

# Create a fixture to provide the AddField instance
@pytest.fixture
def add_field_instance():
    return AddField(model_name="User", name="email", field=None, preserve_default=False)

def test_migration_name_fragment(add_field_instance):
    expected_fragment = "user_email"
    assert add_field_instance.migration_name_fragment() == expected_fragment

def test_migration_name_fragment_with_different_name():
    add_field_instance = AddField(model_name="User", name="username", field=None, preserve_default=False)
    expected_fragment = "user_username"
    assert add_field_instance.migration_name_fragment() == expected_fragment

def test_migration_name_fragment_with_different_model():
    add_field_instance = AddField(model_name="Profile", name="bio", field=None, preserve_default=False)
    expected_fragment = "profile_bio"
    assert add_field_instance.migration_name_fragment() == expected_fragment