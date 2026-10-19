import pytest
from django.db import models
from django.db.migrations import Migration
from django.db.migrations.operations import CreateModel, AddField, AddIndex, AddConstraint, AlterUniqueTogether, AlterIndexTogether, AlterOrderWithRespectTo
from django.contrib.auth.models import User
from django.db.migrations.autodetector import MigrationAutodetector

class TestMigrationAutodetector:
    @pytest.fixture
    def setup_migration_autodetector(self):
        # State setup for the MigrationAutodetector
        from_state = Migration('0001_initial', 'app')
        to_state = Migration('0002_auto', 'app')
        autodetector = MigrationAutodetector(from_state, to_state, None)
        autodetector.old_model_keys = set()
        autodetector.old_unmanaged_keys = set()
        autodetector.new_model_keys = {('app', 'NewModel')}
        autodetector.new_unmanaged_keys = set()
        
        # Define a new model dynamically
        class NewModel(models.Model):
            name = models.CharField(max_length=255)

        autodetector.new_apps = models.AppConfig.create('app', 'app')
        autodetector.new_apps.models['app.NewModel'] = NewModel
        autodetector.to_state.models[('app', 'NewModel')] = autodetector.new_apps.get_model('app', 'NewModel')._meta

        yield autodetector

    def test_generate_created_models(self, setup_migration_autodetector):
        autodetector = setup_migration_autodetector
        
        # Execute the method under test
        autodetector.generate_created_models()
        
        # Assert the operations added
        assert len(autodetector.operations) == 1
        assert isinstance(autodetector.operations[0], CreateModel)
        assert autodetector.operations[0].name == 'NewModel'
        
        # Verify fields in CreateModel operation
        assert len(autodetector.operations[0].fields) == 1
        assert autodetector.operations[0].fields[0][0] == 'name'
        
        # Check dependencies are set properly
        assert len(autodetector.operations[0].dependencies) == 1
        assert autodetector.operations[0].dependencies[0] == ('app', 'NewModel', None, False)

    def test_generate_created_models_with_relations(self, setup_migration_autodetector):
        autodetector = setup_migration_autodetector
        
        # Add a related field example
        class RelatedModel(models.Model):
            user = models.ForeignKey(User, on_delete=models.CASCADE)
        
        autodetector.new_apps.models['app.RelatedModel'] = RelatedModel
        autodetector.to_state.models[('app', 'RelatedModel')] = autodetector.new_apps.get_model('app', 'RelatedModel')._meta
        
        autodetector.new_model_keys.add(('app', 'RelatedModel'))
        
        # Execute the method under test again
        autodetector.generate_created_models()
        
        # Verify the CreateModel and AddField operations
        assert len(autodetector.operations) >= 2  # Should include both NewModel and RelatedModel
        assert any(isinstance(op, AddField) for op in autodetector.operations)
        
        # Check that connected operations are correctly identified
        related_field_ops = [
            op for op in autodetector.operations if isinstance(op, AddField)
        ]
        assert len(related_field_ops) > 0