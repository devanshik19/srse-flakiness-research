import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class ExampleModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

@pytest.fixture
def editor():
    class TestEditor(BaseDatabaseSchemaEditor):
        def quote_name(self, name):
            return name
        
    return TestEditor(None, False)

def test_field_should_be_altered(editor):
    old_field = ExampleModel._meta.get_field('name')
    new_field_name_changed = models.CharField(max_length=100, verbose_name='New Name')
    new_field_type_changed = models.IntegerField()
    new_field_additional_attr = models.CharField(max_length=100, db_column='name', help_text='New Help Text')

    assert editor._field_should_be_altered(old_field, new_field_name_changed) is True
    assert editor._field_should_be_altered(old_field, new_field_type_changed) is True
    assert editor._field_should_be_altered(old_field, new_field_additional_attr) is False

    new_field_same = models.CharField(max_length=100)
    assert editor._field_should_be_altered(old_field, new_field_same) is False