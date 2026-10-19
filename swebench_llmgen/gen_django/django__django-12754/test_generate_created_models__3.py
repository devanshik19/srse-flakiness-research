import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations import operations
from django.db.migrations.state import ProjectState
from django.db.migrations.autodetector import MigrationAutodetector

class TestMigrationAutodetector:
    @pytest.fixture(autouse=True)
    def setup_method(self, settings):
        # Setting up the necessary states
        self.old_model_keys = set()
        self.old_unmanaged_keys = set()
        self.new_model_keys = {('auth', 'user')}
        self.new_unmanaged_keys = set()
        
        self.old_proxy_keys = set()
        
        model_states = {
            ('auth', 'user'): ProjectState(model={'auth.User': User}),
        }
        self.to_state = ProjectState(apps=model_states)
        self.from_state = ProjectState(apps={})
        
        self.detector = MigrationAutodetector(self.from_state, self.to_state, None)

    def test_generate_created_models(self):
        # Add a new model to simulate addition
        self.detector.new_apps = self.to_state
        
        self.detector.generate_created_models()

        # Check if operations were added for creating the User model
        operations_list = self.detector.ops
        assert any(isinstance(op, operations.CreateModel) and op.name == 'User' for op in operations_list)

        # Check if fields were correctly added
        user_model_ops = [op for op in operations_list if isinstance(op, operations.AddField) and op.model_name == 'User']
        assert len(user_model_ops) > 0

        # Ensure dependencies are correct
        for op in user_model_ops:
            assert (op.model_name, op.name) in self.detector.old_model_keys or (op.model_name, op.name) in self.detector.new_model_keys