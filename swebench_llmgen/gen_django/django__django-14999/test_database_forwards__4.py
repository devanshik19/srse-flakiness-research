import pytest
from django.contrib.auth.models import User
from django.db import migrations, models
from django.db.migrations.operations.models import CreateModel


@pytest.mark.parametrize("model_fields", [
    {'username': models.CharField(max_length=150, unique=True)},
    {'email': models.EmailField(unique=True)},
])
def test_database_forwards(model_fields, settings):
    class TestCreateModel(CreateModel):
        def __init__(self, name="TestModel", fields=model_fields, options=None, bases=None, managers=None):
            super().__init__(name, fields, options, bases, managers)

    app_label = 'auth'
    schema_editor = migrations.RunPython.noop
    from_state = migrations.State()
    to_state = migrations.State()

    # Register the model in the state
    test_model = TestCreateModel(name='User', fields=model_fields)
    to_state.apps = migrations.State()
    to_state.apps.register_model(app_label, 'User', test_model)
    
    # Ensure the model can be created
    test_create_model = TestCreateModel(name='User', fields=model_fields)
    test_create_model.database_forwards(app_label, schema_editor, from_state, to_state)

    model = to_state.apps.get_model(app_label, 'User')
    assert model is not None
    assert hasattr(model, 'username') and isinstance(getattr(model, 'username'), models.CharField)
    assert hasattr(model, 'email') and isinstance(getattr(model, 'email'), models.EmailField)

    # Test create_model to be called
    existing_user = User(username='testuser', email='test@example.com')
    existing_user.save()
    assert User.objects.filter(username='testuser').exists()