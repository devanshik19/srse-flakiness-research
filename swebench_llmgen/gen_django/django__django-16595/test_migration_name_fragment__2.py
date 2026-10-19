import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.fields import AddField

class TestAddField:
    
    def test_migration_name_fragment(self):
        model_name = 'User'
        name = 'email'
        field = User._meta.get_field('email')
        preserve_default = NOT_PROVIDED
        
        add_field_operation = AddField(model_name, name, field, preserve_default)
        add_field_operation.model_name_lower = model_name.lower()
        add_field_operation.name_lower = name.lower()
        
        expected_fragment = "user_email"
        assert add_field_operation.migration_name_fragment() == expected_fragment