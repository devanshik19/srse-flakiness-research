import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestBaseDatabaseSchemaEditor:

    @pytest.fixture
    def editor(self):
        connection = None  # Replace with actual database connection if needed
        return BaseDatabaseSchemaEditor(connection, collect_sql=False)

    @pytest.fixture
    def old_field(self):
        return User._meta.get_field('username')

    @pytest.fixture
    def new_field_same_name(self):
        return User._meta.get_field('username')

    @pytest.fixture
    def new_field_different_name(self):
        field = User._meta.get_field('username').deconstruct()
        field[-1]['name'] = 'new_username'
        return models.Field.from_db_value(*field)

    @pytest.fixture
    def new_field_with_db_column(self):
        field = User._meta.get_field('username').deconstruct()
        field[-1]['db_column'] = 'user_name'
        return models.Field.from_db_value(*field)

    def test_field_should_not_be_altered_when_name_is_changed(self, editor, old_field, new_field_same_name):
        assert not editor._field_should_be_altered(old_field, new_field_same_name)

    def test_field_should_be_altered_when_field_name_different(self, editor, old_field, new_field_different_name):
        assert editor._field_should_be_altered(old_field, new_field_different_name)

    def test_field_should_not_be_altered_when_db_column_is_added(self, editor, old_field, new_field_with_db_column):
        assert not editor._field_should_be_altered(old_field, new_field_with_db_column)

    def test_field_should_be_altered_when_type_changed(self, editor, old_field):
        new_field = models.CharField(max_length=100)  # Example of a different field type
        assert editor._field_should_be_altered(old_field, new_field)