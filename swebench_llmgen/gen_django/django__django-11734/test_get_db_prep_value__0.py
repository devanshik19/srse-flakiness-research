import pytest
from django.contrib.auth.models import User
from django.db import models

class TestField(models.Field):
    def get_prep_value(self, value):
        return str(value) if value is not None else None

def test_get_db_prep_value():
    field = TestField()

    # Test case where value is None and prepared is False
    value = None
    connection = None  # No actual connection needed for this test
    result = field.get_db_prep_value(value, connection, prepared=False)
    assert result is None

    # Test case where value is a string and prepared is False
    value = 'test'
    result = field.get_db_prep_value(value, connection, prepared=False)
    assert result == 'test'

    # Test case where value is already prepared (string)
    value = 'already prepared'
    result = field.get_db_prep_value(value, connection, prepared=True)
    assert result == 'already prepared'

    # Test case where value is int and prepared is False
    value = 123
    result = field.get_db_prep_value(value, connection, prepared=False)
    assert result == '123'

    # Test case where value is datetime object and prepared is False
    value = User.objects.create(username='testuser')  # Use User model for actual instance
    result = field.get_db_prep_value(value, connection, prepared=False)
    assert result == 'testuser'