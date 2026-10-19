import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector

# Helper function to create a mock field with a remote_field
def create_mock_field(remote_model=None):
    class MockField(models.Field):
        def __init__(self, *args, **kwargs):
            self.remote_field = self.RemoteField(remote_model)
            super().__init__(*args, **kwargs)

        class RemoteField:
            def __init__(self, model):
                self.model = model
        
    return MockField()

def test_only_relation_agnostic_fields():
    # Setup
    autodetector = MigrationAutodetector(None, None, None)
    
    # Test fields without relationships
    fields = {
        'username': models.CharField(max_length=150),
        'email': models.EmailField(),
        'password': create_mock_field(),
    }
    
    # Test fields with a related model
    related_fields = {
        'profile_picture': create_mock_field(remote_model='auth.User'),
        'login_history': create_mock_field(remote_model='auth.User'),
    }
    
    # Combining all fields
    all_fields = {**fields, **related_fields}

    # Call the method
    result = autodetector.only_relation_agnostic_fields(all_fields)
    
    # Verify the result
    assert len(result) == len(all_fields)
    assert all('to' not in deconstruction[2] for deconstruction in result if len(deconstruction) > 2)
    assert all(deconstruction[0] in fields or deconstruction[0] in related_fields for deconstruction in result)