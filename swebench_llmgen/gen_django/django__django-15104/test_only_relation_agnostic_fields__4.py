import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector

@pytest.fixture
def migration_autodetector():
    # Creating a mock MigrationAutodetector with dummy state
    return MigrationAutodetector(None, None, None)

def test_only_relation_agnostic_fields(migration_autodetector):
    # Creating a sample field with a remote field
    class RelatedModel(models.Model):
        pass

    related_field = models.ForeignKey(RelatedModel, on_delete=models.CASCADE, related_name='related')

    # Creating a sample model
    class TestModel(models.Model):
        field_1 = models.CharField(max_length=10)
        field_2 = related_field

    fields = {
        'field_1': TestModel._meta.get_field('field_1'),
        'field_2': TestModel._meta.get_field('field_2'),
    }

    # Call the focal method
    result = migration_autodetector.only_relation_agnostic_fields(fields)

    # Expected result after removing the 'to' from deep_deconstruct of field_2
    expected_result = [
        migration_autodetector.deep_deconstruct(TestModel._meta.get_field('field_1')),
        migration_autodetector.deep_deconstruct(TestModel._meta.get_field('field_2'))
    ]

    # Remove the 'to' field from field_2's deconstructed value
    expected_result[1][2].pop('to', None)

    assert result == expected_result