import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector

@pytest.fixture
def autodetector():
    return MigrationAutodetector(None, None, None)

@pytest.fixture
def user_field():
    return User._meta.get_field('username')

def test_only_relation_agnostic_fields_with_related_field(autodetector, user_field):
    # Simulating a field with a related field
    user_field.remote_field.model = User
    
    fields = {
        'username': user_field,
        'email': User._meta.get_field('email'),
    }
    
    result = autodetector.only_relation_agnostic_fields(fields)
    
    # Check that the 'to' field is removed from related field deconstruction
    assert isinstance(result, list)
    assert len(result) == 2
    
    # Verify that the remote field reference is not included in the output for 'username'
    assert 'to' not in result[0][2]
    assert 'to' in result[1][2]  # The 'email' field should still have all details

def test_only_relation_agnostic_fields_without_related_field(autodetector):
    # Simulating a field without a related field
    fields = {
        'first_name': models.CharField(max_length=30),
        'last_name': models.CharField(max_length=30),
    }

    result = autodetector.only_relation_agnostic_fields(fields)
    
    assert isinstance(result, list)
    assert len(result) == 2
    
    # Check that both fields are included and have full deconstruction
    assert 'to' in result[0][2]
    assert 'to' in result[1][2]