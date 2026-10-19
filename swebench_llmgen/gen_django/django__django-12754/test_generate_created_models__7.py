import pytest
from django.db import models
from django.db.migrations import operations
from django.db.migrations.state import ProjectState
from django.db.migrations.autodetector import MigrationAutodetector

# Create a model for testing
class TestModel(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    
class TestRelatedModel(models.Model):
    test_model = models.ForeignKey(TestModel, on_delete=models.CASCADE, related_name='related_models')

def test_generate_created_models():
    from_state = ProjectState()
    to_state = ProjectState()
    
    # Setting the initial state with current models
    from_state.models['app_name.TestModel'] = (TestModel, None, 'app_name')
    
    # New state with an additional model
    to_state.models['app_name.TestModel'] = (TestModel, None, 'app_name')
    to_state.models['app_name.TestRelatedModel'] = (TestRelatedModel, None, 'app_name')

    autodetector = MigrationAutodetector(from_state, to_state, None)
    
    autodetector.generate_created_models()

    operations = autodetector.get_operations()

    assert len(operations) == 2  # We expect two create operations
    assert isinstance(operations[0], operations.CreateModel)
    assert operations[0].name == 'TestModel'
    assert isinstance(operations[1], operations.CreateModel)
    assert operations[1].name == 'TestRelatedModel'
    
    # Check if correct fields for TestRelatedModel are being added
    assert len(operations[1].fields) == 1  # TestRelatedModel should have a FK
    assert operations[1].fields[0][0] == 'test_model'  # The foreign key field

    # Add additional checks and assertions if necessary to cover more branches and logic