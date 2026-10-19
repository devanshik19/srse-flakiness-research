import pytest
from django.contrib.auth.models import User
from your_module_path import AddField  # Replace 'your_module_path' with the actual path to AddField

@pytest.mark.parametrize("model_name, name, expected_fragment", [
    ("User", "username", "user_username"),
    ("User", "email", "user_email"),
    ("User", "first_name", "user_first_name"),
])
def test_migration_name_fragment(model_name, name, expected_fragment):
    field = None  # This can be None or a mock, as it's not used in the fragment generation.
    add_field_operation = AddField(model_name=model_name, name=name, field=field, preserve_default=NOT_PROVIDED)
    
    assert add_field_operation.migration_name_fragment() == expected_fragment