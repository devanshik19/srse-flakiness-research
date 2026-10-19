import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor

@pytest.fixture
def setup_models():
    class TestModel(models.Model):
        name = models.CharField(max_length=100)

    # Create the initial schema
    TestModel.objects.create(name="Initial")
    return TestModel

def test_alter_field_rename_column(setup_models):
    editor = DatabaseSchemaEditor(connection=None)  # Mock or real connection if needed
    model = setup_models
    old_field = model._meta.get_field('name')
    new_field = models.CharField(max_length=255, name='new_name')

    editor._alter_field(
        model=model,
        old_field=old_field,
        new_field=new_field,
        old_type='CharField',
        new_type='CharField',
        old_db_params={},
        new_db_params={},
        strict=False,
    )

    modified_instance = model.objects.get(pk=1)
    assert modified_instance.new_name == "Initial"

def test_alter_field_recreate_table(setup_models):
    editor = DatabaseSchemaEditor(connection=None)
    model = setup_models
    old_field = model._meta.get_field('name')
    new_field = models.IntegerField(name='name')  # Changing type to IntegerField

    editor._alter_field(
        model=model,
        old_field=old_field,
        new_field=new_field,
        old_type='CharField',
        new_type='IntegerField',
        old_db_params={},
        new_db_params={},
        strict=False,
    )

    # Verifying that the table has been recreated (this would require inspecting the schema)
    assert 'name' not in model._meta.get_fields()
    assert 'name' in model._meta.get_fields(include_hidden=True)  # Check for new field visibility