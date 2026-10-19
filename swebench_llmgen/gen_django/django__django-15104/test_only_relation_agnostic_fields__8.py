import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector

@pytest.fixture
def migration_autodetector():
    from_state = None  # Assuming None for simplicity in this fixture
    to_state = None    # Assuming None for simplicity in this fixture
    questioner = None  # Assuming None for simplicity in this fixture
    return MigrationAutodetector(from_state, to_state, questioner)

def test_only_relation_agnostic_fields_no_related_fields(migration_autodetector):
    fields = {
        'username': User._meta.get_field('username'),
        'email': User._meta.get_field('email'),
    }
    expected = [
        migration_autodetector.deep_deconstruct(User._meta.get_field('email')),
        migration_autodetector.deep_deconstruct(User._meta.get_field('username')),
    ]
    result = migration_autodetector.only_relation_agnostic_fields(fields)
    assert result == expected

def test_only_relation_agnostic_fields_with_related_fields(migration_autodetector):
    # Custom field definition with a remote field
    class RelatedModel(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)

    fields = {
        'related_user': RelatedModel._meta.get_field('user'),
    }
    expected_deconstruction = migration_autodetector.deep_deconstruct(RelatedModel._meta.get_field('user'))
    del expected_deconstruction[2]['to']

    expected = [expected_deconstruction]
    result = migration_autodetector.only_relation_agnostic_fields(fields)
    assert result == expected

def test_only_relation_agnostic_fields_empty(migration_autodetector):
    fields = {}
    expected = []
    result = migration_autodetector.only_relation_agnostic_fields(fields)
    assert result == expected