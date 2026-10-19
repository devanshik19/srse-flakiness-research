import pytest
from django.db import models
from django.contrib.auth.models import User
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    connection = User._meta.db_table
    return BaseDatabaseSchemaEditor(connection, collect_sql=False)

def test_field_should_be_altered_name_change(schema_editor):
    old_field = User._meta.get_field('username')
    new_field = User._meta.get_field('username')
    new_field.set_attributes_from_name('new_username')
    
    assert schema_editor._field_should_be_altered(old_field, new_field) is True

def test_field_should_be_altered_db_column_change(schema_editor):
    old_field = User._meta.get_field('email')
    new_field = User._meta.get_field('email')
    new_field.db_column = 'new_email_column'
    
    assert schema_editor._field_should_be_altered(old_field, new_field) is True

def test_field_should_not_be_altered_same_field(schema_editor):
    old_field = User._meta.get_field('first_name')
    new_field = User._meta.get_field('first_name')
    
    assert schema_editor._field_should_be_altered(old_field, new_field) is False

def test_field_should_be_altered_type_change(schema_editor):
    old_field = User._meta.get_field('last_name')
    new_field = models.CharField(max_length=150, verbose_name='Last Name')
    
    # Simulating a type change
    old_field.set_attributes_from_name('last_name')
    new_field.set_attributes_from_name('last_name')
    
    assert schema_editor._field_should_be_altered(old_field, new_field) is True

def test_field_should_not_be_altered_non_database_attr_change(schema_editor):
    old_field = User._meta.get_field('email')
    new_field = User._meta.get_field('email')
    new_field.help_text = 'New help text'
    
    assert schema_editor._field_should_be_altered(old_field, new_field) is False