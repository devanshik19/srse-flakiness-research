import pytest
from django.contrib.auth.models import User
from django.db import migrations
from django.db.migrations.autodetector import MigrationAutodetector


@pytest.fixture
def setup_migration_autodetector():
    from_state = migrations.state.State()
    to_state = migrations.state.State()
    questioner = None  # No need for questioner in this test.
    autodetector = MigrationAutodetector(from_state, to_state, questioner)
    
    # Set up some initial state
    # Assuming we're populating old and new models for the test
    autodetector.old_model_keys = set()
    autodetector.old_unmanaged_keys = set()
    autodetector.new_model_keys = {('auth', 'User')}  # Existing User model
    autodetector.new_unmanaged_keys = set()
    
    # Prepare to_state to reflect the addition of a new model
    model_state = migrations.state.ModelState(
        'User',
        fields=(('username', models.CharField(max_length=150)),),
        options={'managed': True},
        bases=()
    )
    autodetector.to_state.models = {('auth', 'User'): model_state}
    
    return autodetector


def test_generate_created_models(setup_migration_autodetector):
    autodetector = setup_migration_autodetector
    autodetector.generate_created_models()

    # Assertions to check if operations are added correctly
    assert len(autodetector.operations) > 0  # Ensure some operations were added
    
    create_model_op = autodetector.operations[0]
    assert isinstance(create_model_op, migrations.operations.CreateModel)
    
    assert create_model_op.name == 'User'
    assert create_model_op.fields == [('username', models.CharField(max_length=150))]

    add_field_ops = [op for op in autodetector.operations if isinstance(op, migrations.operations.AddField)]
    assert len(add_field_ops) == 0  # No AddField should be there for field relationships initially

    # Now assume creating foreign key or m2m relationships
    user_model = User._meta
    autodetector.to_state.models[('auth', 'User')].local_fields.append(user_model.fields['groups'])
    autodetector.generate_created_models()  # Run again to capture relationships
    
    add_field_ops = [op for op in autodetector.operations if isinstance(op, migrations.operations.AddField)]
    assert len(add_field_ops) == 1  # Should now include an AddField for the relationships
    assert add_field_ops[0].name == 'groups'
    
    # Check indexes and other options
    assert any(isinstance(op, migrations.operations.AddIndex) for op in autodetector.operations) == False