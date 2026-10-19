import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.fields import AddField

def test_migration_name_fragment():
    model_name = 'User'
    field_name = 'email'
    field = NOT_PROVIDED
    preserve_default = False
    
    add_field_operation = AddField(model_name=model_name, name=field_name, field=field, preserve_default=preserve_default)
    
    expected_fragment = "user_email"
    assert add_field_operation.migration_name_fragment() == expected_fragment