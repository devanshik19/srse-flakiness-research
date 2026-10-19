import pytest
from django.contrib.auth.models import User
from django.db.models import CharField

class TestBaseDatabaseSchemaEditor:

    @pytest.fixture
    def editor(self):
        # Create an instance of BaseDatabaseSchemaEditor
        from django.db.backends.base.schema import BaseDatabaseSchemaEditor
        return BaseDatabaseSchemaEditor(connection=None, collect_sql=False)

    def test_field_should_be_altered_different_columns(self, editor):
        old_field = CharField(column='old_name')
        new_field = CharField(column='new_name')
        assert editor._field_should_be_altered(old_field, new_field) is True

    def test_field_should_be_altered_same_columns_diff_attrs(self, editor):
        old_field = CharField(column='name', max_length=100)
        new_field = CharField(column='name', max_length=200)
        assert editor._field_should_be_altered(old_field, new_field) is True

    def test_field_should_be_altered_same_columns_same_attrs(self, editor):
        old_field = CharField(column='name', max_length=100)
        new_field = CharField(column='name', max_length=100)
        assert editor._field_should_be_altered(old_field, new_field) is False

    def test_field_should_be_altered_different_non_database_attrs(self, editor):
        old_field = CharField(column='name', db_column='name', blank=False)
        new_field = CharField(column='name', db_column='name', blank=True)
        assert editor._field_should_be_altered(old_field, new_field) is False

    def test_field_should_be_altered_different_field_name(self, editor):
        old_field = CharField(column='name')
        new_field = CharField(column='name', db_column='new_name')
        assert editor._field_should_be_altered(old_field, new_field) is True