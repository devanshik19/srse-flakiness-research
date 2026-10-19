import collections.abc
import pytest
from django.db import models
from django.contrib.auth.models import User

class TestField(models.Field):
    def __init__(self):
        super().__init__(verbose_name='Test Field', name='test_field', primary_key=False, max_length=255)

@pytest.fixture
def test_field():
    return TestField()

def test_deconstruct(test_field):
    field_name, path, args, kwargs = test_field.deconstruct()

    assert field_name == 'test_field'
    assert path == 'django.db.models.fields.tests.TestField'
    assert args == []
    assert kwargs['verbose_name'] == 'Test Field'
    assert kwargs['max_length'] == 255
    assert kwargs['primary_key'] is False
    assert kwargs['unique'] is False
    assert kwargs['blank'] is False
    assert kwargs['null'] is False
    assert kwargs['db_index'] is False
    assert kwargs['default'] == models.NOT_PROVIDED
    assert kwargs['editable'] is True
    assert kwargs['serialize'] is True
    assert kwargs['unique_for_date'] is None
    assert kwargs['unique_for_month'] is None
    assert kwargs['unique_for_year'] is None
    assert kwargs['choices'] is None
    assert kwargs['help_text'] == ''
    assert kwargs['db_column'] is None
    assert kwargs['db_tablespace'] is None
    assert kwargs['auto_created'] is False
    assert kwargs['validators'] == []
    assert kwargs['error_messages'] is None