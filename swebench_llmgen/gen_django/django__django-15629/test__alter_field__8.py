import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor

@pytest.mark.django_db
def test_alter_field_rename_column():
    # Arrange
    class ExampleModel(models.Model):
        name = models.CharField(max_length=100)
        
    # Create necessary database tables
    ExampleModel.objects.create(name='Test User')

    # Get the schema editor
    editor = DatabaseSchemaEditor(connection=User._state.db)

    old_field = ExampleModel._meta.get_field('name')
    new_field = models.CharField(max_length=200, verbose_name='renamed_name')
    
    # Act
    editor._alter_field(
        model=ExampleModel,
        old_field=old_field,
        new_field=new_field,
        old_type=old_field.get_internal_type(),
        new_type=new_field.get_internal_type(),
        old_db_params={},
        new_db_params={},
        strict=False,
    )

    # Assert
    updated_model = ExampleModel.objects.get(id=1)
    assert updated_model._meta.get_field('name').max_length == 200

@pytest.mark.django_db
def test_alter_field_remake_table():
    # Arrange
    class AnotherModel(models.Model):
        age = models.IntegerField()

    AnotherModel.objects.create(age=25)

    editor = DatabaseSchemaEditor(connection=User._state.db)

    old_field = AnotherModel._meta.get_field('age')
    new_field = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='age_decimal')

    # Act
    editor._alter_field(
        model=AnotherModel,
        old_field=old_field,
        new_field=new_field,
        old_type=old_field.get_internal_type(),
        new_type=new_field.get_internal_type(),
        old_db_params={},
        new_db_params={},
        strict=False,
    )

    # Assert
    updated_model = AnotherModel.objects.get(id=1)
    assert isinstance(updated_model.age, Decimal)