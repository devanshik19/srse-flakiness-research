import pytest
from django.contrib.auth.models import User
from django.db import models

class TestField(models.Field):
    def get_prep_value(self, value):
        if value is None:
            return value
        return str(value)

def test_get_db_prep_value_with_none():
    field = TestField()
    value = None
    connection = None  # Mock connection as it's not used in the test
    result = field.get_db_prep_value(value, connection, prepared=False)
    assert result is None

def test_get_db_prep_value_with_prepared_value():
    field = TestField()
    value = 'test_value'
    connection = None  # Mock connection as it's not used in the test
    result = field.get_db_prep_value(value, connection, prepared=True)
    assert result == value

def test_get_db_prep_value_with_unprepared_value():
    field = TestField()
    value = 'test_value'
    connection = None  # Mock connection as it's not used in the test
    result = field.get_db_prep_value(value, connection, prepared=False)
    assert result == 'test_value'  # Check if get_prep_value is applied

def test_get_db_prep_value_with_user_instance():
    field = TestField()
    user = User(username='test_user')
    connection = None  # Mock connection as it's not used in the test
    result = field.get_db_prep_value(user, connection, prepared=False)
    assert result == 'test_user'  # Check if user object is converted to string