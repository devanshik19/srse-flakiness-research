import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestBaseDatabaseSchemaEditor:

    @pytest.fixture
    def editor(self):
        return BaseDatabaseSchemaEditor(None, collect_sql=False)

    @pytest.fixture
    def old_field(self):
        return User._meta.get_field('username')

    @pytest.fixture
    def new_field(self):
        return User._meta.get_field('email')

    def test_field_should_be_altered_different_columns(self, editor, old_field, new_field):
        assert editor._field_should_be_altered(old_field, new_field) is True

    def test_field_should_be_altered_same_columns(self, editor, old_field, new_field):
        new_field_copy = User._meta.get_field('username')
        assert editor._field_should_be_altered(old_field, new_field_copy) is False

    def test_field_should_be_altered_same_name_different_options(self, editor, old_field):
        new_field = models.CharField(max_length=30, unique=True)
        old_field_copy = old_field.clone()  # Assuming there's a method to clone field
        assert editor._field_should_be_altered(old_field_copy, new_field) is True

    def test_field_should_not_be_altered_on_non_db_attributes(self, editor, old_field):
        new_field = models.CharField(max_length=150, blank=True)
        assert editor._field_should_be_altered(old_field, new_field) is False