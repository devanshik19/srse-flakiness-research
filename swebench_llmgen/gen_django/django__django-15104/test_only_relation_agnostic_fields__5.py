import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector

@pytest.fixture
def migration_autodetector():
    return MigrationAutodetector(None, None, None)

def test_only_relation_agnostic_fields(migration_autodetector):
    # Prepare fields with related and non-related fields.
    fields = {
        'username': User._meta.get_field('username'),
        'email': User._meta.get_field('email'),
        'groups': User._meta.get_field('groups'),  # This field has a relation.
        'is_active': User._meta.get_field('is_active'),
    }

    # Deep deconstruct will be invoked within only_relation_agnostic_fields, we'll need it to simulate behavior.
    def deep_deconstruct_mock(field):
        if field.name == 'groups':
            return (field.name, field.__class__, {}, {'to': 'auth.Group'})  # Simulating related field structure
        return (field.name, field.__class__, {}, {})  # For non-related fields

    # Patch deep_deconstruct to our mock
    migration_autodetector.deep_deconstruct = deep_deconstruct_mock

    # Call the focal function
    result = migration_autodetector.only_relation_agnostic_fields(fields)

    # Assertions
    assert len(result) == 4
    assert result[0][2].get('to') is None  # 'username' should not have 'to'
    assert result[1][2].get('to') is None  # 'email' should not have 'to'
    assert result[2][2].get('to') is None  # 'groups' should not have 'to' after processing
    assert result[3][2].get('to') is None  # 'is_active' should not have 'to'