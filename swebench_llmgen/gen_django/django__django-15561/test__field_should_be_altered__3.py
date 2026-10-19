import pytest
from django.contrib.auth.models import User
from django.db.models import CharField
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestBaseDatabaseSchemaEditor:

    @pytest.fixture
    def schema_editor(self):
        connection = None  # Mock or pass a real connection if needed
        return BaseDatabaseSchemaEditor(connection, False)

    def test_field_should_be_altered_when_column_names_differs(self, schema_editor):
        old_field = CharField(column='old_name')
        new_field = CharField(column='new_name')
        assert schema_editor._field_should_be_altered(old_field, new_field)

    def test_field_should_not_be_altered_when_only_name_changes(self, schema_editor):
        old_field = CharField(column='name')
        new_field = CharField(column='new_name')
        assert not schema_editor._field_should_be_altered(old_field, new_field)

    def test_field_should_not_be_altered_when_non_database_attributes_change(self, schema_editor):
        old_field = CharField(column='name', db_column='custom_name', blank=True)
        new_field = CharField(column='name', db_column='new_custom_name', blank=True)
        assert not schema_editor._field_should_be_altered(old_field, new_field)

    def test_field_should_be_altered_when_other_attributes_change(self, schema_editor):
        old_field = CharField(column='name', max_length=100)
        new_field = CharField(column='name', max_length=200)
        assert schema_editor._field_should_be_altered(old_field, new_field)

    def test_field_should_alter_when_adding_db_column(self, schema_editor):
        old_field = CharField(column='name')
        new_field = CharField(column='name', db_column='new_column')
        assert schema_editor._field_should_be_altered(old_field, new_field)