import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector

@pytest.fixture
def autodetector():
    return MigrationAutodetector(None, None, None)

def test_only_relation_agnostic_fields_with_related_fields(autodetector):
    # Define model fields with related fields
    class RelatedModel(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    fields = {
        'user': RelatedModel._meta.get_field('user'),
    }
    
    result = autodetector.only_relation_agnostic_fields(fields)
    
    assert len(result) == 1
    assert 'to' not in result[0][2]

def test_only_relation_agnostic_fields_without_related_fields(autodetector):
    # Define a model field without related fields
    class SimpleModel(models.Model):
        username = models.CharField(max_length=150)
    
    fields = {
        'username': SimpleModel._meta.get_field('username'),
    }
    
    result = autodetector.only_relation_agnostic_fields(fields)
    
    assert len(result) == 1
    assert result[0][1].name == 'username'
    assert 'to' not in result[0][2]  # Ensure 'to' is not present