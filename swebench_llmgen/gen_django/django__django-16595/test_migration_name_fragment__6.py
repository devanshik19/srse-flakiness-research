import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.operations.fields import AddField

class TestAddField:
    def setup_method(self):
        self.model_name = 'User'
        self.name = 'age'
        self.field = models.IntegerField()
        self.preserve_default = NOT_PROVIDED
        self.add_field_operation = AddField(self.model_name, self.name, self.field, self.preserve_default)

    def test_migration_name_fragment(self):
        expected_fragment = "user_age"
        actual_fragment = self.add_field_operation.migration_name_fragment()
        assert actual_fragment == expected_fragment

    def test_migration_name_fragment_with_different_field_name(self):
        self.add_field_operation.name = 'username'
        expected_fragment = "user_username"
        actual_fragment = self.add_field_operation.migration_name_fragment()
        assert actual_fragment == expected_fragment