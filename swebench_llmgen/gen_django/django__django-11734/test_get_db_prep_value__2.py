import pytest
from django.contrib.auth.models import User
from django.db import models

class TestField(models.Field):
    def get_prep_value(self, value):
        if value is None:
            return value
        return str(value)

def test_get_db_prep_value():
    # Arrange
    field = TestField()
    connection = models.connections['default']
    
    # Test case 1: When 'prepared' is False, should call get_prep_value
    value_to_prepare = 123
    prepared_value = field.get_db_prep_value(value_to_prepare, connection, prepared=False)
    assert prepared_value == '123'  # Should return the string representation of the integer
    
    # Test case 2: When 'prepared' is True, should return the value as-is
    prepared_value_true = field.get_db_prep_value(value_to_prepare, connection, prepared=True)
    assert prepared_value_true == 123  # Should return the original integer value

    # Test case 3: Testing with None value
    none_value_prepared = field.get_db_prep_value(None, connection, prepared=False)
    assert none_value_prepared is None  # Should return None

    none_value_prepared_true = field.get_db_prep_value(None, connection, prepared=True)
    assert none_value_prepared_true is None  # Should return None