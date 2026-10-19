import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.operations import CreateModel, AddField, AddIndex, AddConstraint, AlterUniqueTogether, AlterIndexTogether, AlterOrderWithRespectTo, AlterField
from django.db.migrations.state import ProjectState
from django.db.migrations.autodetector import MigrationAutodetector


class DummyMigrationAutodetector(MigrationAutodetector):
    def __init__(self, from_state=None, to_state=None, questioner=None):
        self.old_model_keys = set()
        self.old_unmanaged_keys = set()
        self.new_model_keys = set()
        self.new_unmanaged_keys = set()
        self.to_state = to_state or ProjectState()
        self.new_apps = self.to_state

        # Call the parent constructor
        super().__init__(from_state, to_state, questioner)

    def add_operation(self, app_label, operation, dependencies=None, beginning=False):
        self.operations.append((app_label, operation))

    def __init__(self, from_state, to_state, questioner):
        super().__init__(from_state, to_state, questioner)
        self.operations = []


@pytest.fixture
def autodetector():
    from_state = ProjectState()
    to_state = ProjectState()
    return DummyMigrationAutodetector(from_state, to_state)


def test_generate_created_models(autodetector):
    # Set up a dummy model
    class DummyModel(models.Model):
        name = models.CharField(max_length=255)

    autodetector.old_model_keys = set()
    autodetector.new_model_keys = {('auth', 'User')}
    autodetector.to_state.models[('auth', 'User')] = DummyModel

    # Run the method to test
    autodetector.generate_created_models()

    # Verify that the operations were added correctly
    assert len(autodetector.operations) > 0

    # Check the type of operations that were added
    created_models_ops = [
        op for app_label, op in autodetector.operations if isinstance(op, CreateModel)
    ]
    assert len(created_models_ops) == 1

    # Check relationships and fields handling
    user_model = autodetector.to_state.models[('auth', 'User')]
    assert hasattr(user_model, 'name')


def test_generate_created_models_unmanaged(autodetector):
    # Set up a dummy unmanaged model
    class UnmanagedModel(models.Model):
        name = models.CharField(max_length=255)

        class Meta:
            managed = False

    autodetector.old_model_keys = set()
    autodetector.new_model_keys = {('app_name', 'UnmanagedModel')}
    autodetector.to_state.models[('app_name', 'UnmanagedModel')] = UnmanagedModel

    # Run the method to test
    autodetector.generate_created_models()

    # Verify that the operations were added correctly
    assert len(autodetector.operations) > 0

    # Check that no database modification operations were added for the unmanaged model
    assert all(not isinstance(op[1], CreateModel) for op in autodetector.operations)