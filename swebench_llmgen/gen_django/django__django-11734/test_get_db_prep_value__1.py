import pytest
from django.contrib.auth.models import User
from django.db import models

class TestField(models.Field):
    def get_prep_value(self, value):
        return super().get_prep_value(value)

def test_get_db_prep_value():
    # Create an instance of the field
    field = TestField()

    # Case 1: When value is None
    db_value = field.get_db_prep_value(None, None, prepared=False)
    assert db_value is None

    # Case 2: When value is a valid integer
    value = 123
    db_value = field.get_db_prep_value(value, None, prepared=False)
    assert db_value == 123

    # Case 3: When value is a valid string
    value = "test"
    db_value = field.get_db_prep_value(value, None, prepared=False)
    assert db_value == "test"

    # Case 4: When prepared is True, we expect the value to stay the same
    value = "prepared_test"
    db_value = field.get_db_prep_value(value, None, prepared=True)
    assert db_value == "prepared_test"

    # Add assertion for User instance
    user_instance = User(username='testuser')
    db_value = field.get_db_prep_value(user_instance, None, prepared=False)
    assert db_value == user_instance