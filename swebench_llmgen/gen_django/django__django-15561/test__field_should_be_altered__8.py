import pytest
from django.db import models
from django.contrib.auth.models import User
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestBaseDatabaseSchemaEditor:

    @pytest.fixture
    def schema_editor(self):
        return BaseDatabaseSchemaEditor(connection=None, collect_sql=False, atomic=False)

    def test_field_should_be_altered_with_different_column_names(self, schema_editor):
        old_field = models.CharField(column='old_name', max_length=100)
        new_field = models.CharField(column='new_name', max_length=100)
        assert schema_editor._field_should_be_altered(old_field, new_field) is True

    def test_field_should_be_altered_with_same_column_names(self, schema_editor):
        old_field = models.CharField(column='name', max_length=100)
        new_field = models.CharField(column='name', max_length=200)
        assert schema_editor._field_should_be_altered(old_field, new_field) is True

    def test_field_should_not_be_altered_for_same_field_name(self, schema_editor):
        old_field = models.CharField(column='name', max_length=100, db_column='custom_name')
        new_field = models.CharField(column='name', max_length=100, db_column='custom_name')
        assert schema_editor._field_should_be_altered(old_field, new_field) is False

    def test_field_should_be_altered_due_to_schema_change(self, schema_editor):
        old_field = models.IntegerField()
        new_field = models.IntegerField(null=True)
        assert schema_editor._field_should_be_altered(old_field, new_field) is True

    def test_field_should_not_be_altered_for_non_database_attributes(self, schema_editor):
        old_field = models.CharField(column='name', max_length=100, blank=True, default='default')
        new_field = models.CharField(column='name', max_length=100, blank=False, default='default')
        assert schema_editor._field_should_be_altered(old_field, new_field) is False