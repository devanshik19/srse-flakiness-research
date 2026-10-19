import pytest
from django.db import models
from django.contrib.auth.models import User
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class CustomField(models.Field):
    def deconstruct(self):
        return ('app.CustomField', self.name, [], {})

class TestBaseDatabaseSchemaEditor:
    def setup_method(self):
        self.editor = BaseDatabaseSchemaEditor(None, False)

    def test_field_should_be_altered_name_change(self):
        old_field = CustomField(name='old_field')
        new_field = CustomField(name='new_field')
        assert self.editor._field_should_be_altered(old_field, new_field) is True

    def test_field_should_not_be_altered_only_related_name_change(self):
        old_field = CustomField(name='field', related_name='old_related')
        new_field = CustomField(name='field', related_name='new_related')
        assert self.editor._field_should_be_altered(old_field, new_field) is False

    def test_field_should_not_be_altered_with_non_db_attr_change(self):
        old_field = CustomField(name='field', db_column='old_column')
        new_field = CustomField(name='field', db_column='old_column', editable=False)
        assert self.editor._field_should_be_altered(old_field, new_field) is False

    def test_field_should_be_altered_column_change(self):
        old_field = CustomField(name='field', db_column='old_column')
        new_field = CustomField(name='field', db_column='new_column')
        assert self.editor._field_should_be_altered(old_field, new_field) is True

    def test_field_should_be_altered_properties_change(self):
        old_field = CustomField(name='field', verbose_name='Old Name')
        new_field = CustomField(name='field', verbose_name='New Name')
        assert self.editor._field_should_be_altered(old_field, new_field) is True