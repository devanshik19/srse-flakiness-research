import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector

@pytest.fixture
def migration_autodetector():
    return MigrationAutodetector(None, None, None)

def test_only_relation_agnostic_fields_empty(migration_autodetector):
    fields = {}
    result = migration_autodetector.only_relation_agnostic_fields(fields)
    assert result == []

def test_only_relation_agnostic_fields_without_remote_field(migration_autodetector):
    class SimpleField(models.Field):
        def deconstruct(self):
            return ('app_label', 'simple_field', 'models.CharField', ())

    fields = {'field1': SimpleField()}
    result = migration_autodetector.only_relation_agnostic_fields(fields)
    assert result == [('app_label', 'simple_field', 'models.CharField', ())]

def test_only_relation_agnostic_fields_with_remote_field(migration_autodetector):
    class RelatedField(models.ForeignKey):
        def deconstruct(self):
            return ('app_label', 'related_field', 'models.ForeignKey', (User,))

    related_field = RelatedField(User, on_delete=models.CASCADE)
    fields = {'field1': related_field}
    result = migration_autodetector.only_relation_agnostic_fields(fields)
    assert result == [('app_label', 'related_field', 'models.ForeignKey', {})]  # without 'to'

def test_only_relation_agnostic_fields_multiple_fields(migration_autodetector):
    class FieldWithRemote(models.ForeignKey):
        def deconstruct(self):
            return ('app_label', 'field_with_remote', 'models.ForeignKey', (User,))

    class FieldWithoutRemote(models.Field):
        def deconstruct(self):
            return ('app_label', 'field_without_remote', 'models.CharField', ())

    fields = {
        'field_with_remote': FieldWithRemote(User, on_delete=models.CASCADE),
        'field_without_remote': FieldWithoutRemote()
    }
    result = migration_autodetector.only_relation_agnostic_fields(fields)
    assert result == [
        ('app_label', 'field_with_remote', 'models.ForeignKey', {}),
        ('app_label', 'field_without_remote', 'models.CharField', ()),
    ]