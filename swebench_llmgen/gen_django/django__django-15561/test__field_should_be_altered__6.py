import pytest
from django.contrib.auth.models import User
from django.db.models import Field, CharField

class TestBaseDatabaseSchemaEditor:
    def setup_method(self):
        self.editor = BaseDatabaseSchemaEditor(None, None, None)

    def test_field_should_be_altered_returns_true_when_columns_differ(self):
        old_field = CharField(column='name')
        new_field = CharField(column='username')
        assert self.editor._field_should_be_altered(old_field, new_field)

    def test_field_should_be_altered_returns_false_when_columns_are_the_same(self):
        old_field = CharField(column='name')
        new_field = CharField(column='name')
        assert not self.editor._field_should_be_altered(old_field, new_field)

    def test_field_should_be_altered_returns_true_when_field_path_diffs(self):
        old_field = CharField(verbose_name='Name')
        new_field = CharField(verbose_name='Full Name')
        assert self.editor._field_should_be_altered(old_field, new_field)

    def test_field_should_be_altered_returns_false_on_non_database_changes(self):
        old_field = CharField(verbose_name='Name', db_column='name')
        new_field = CharField(verbose_name='Name', db_column='name')
        assert not self.editor._field_should_be_altered(old_field, new_field)

    def test_field_should_be_altered_correctly_handles_non_database_attrs(self):
        old_field = CharField(blank=True, db_column='email', max_length=100)
        new_field = CharField(blank=True, db_column='email', max_length=200)
        assert self.editor._field_should_be_altered(old_field, new_field)