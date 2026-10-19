import collections.abc
from django.db import models
from django.contrib.auth.models import User
import pytest

class TestField(models.Field):
    def __init__(self, verbose_name=None, name=None, primary_key=False, max_length=None, unique=False, blank=False, null=False, db_index=False, default=None, editable=True, serialize=True, unique_for_date=None, unique_for_month=None, unique_for_year=None, choices=None, help_text='', db_column=None, db_tablespace=None, auto_created=False, validators=None, error_messages=None):
        super().__init__(verbose_name, name, primary_key, max_length, unique, blank, null, db_index, default, editable, serialize, unique_for_date, unique_for_month, unique_for_year, choices, help_text, db_column, db_tablespace, auto_created, validators, error_messages)

def test_deconstruct():
    field = TestField(name='test_field', verbose_name='Test Field', max_length=255, unique=True)
    field.overrides = {
        "_unique": field.unique,
        "_verbose_name": field.verbose_name,
    }

    name, path, args, keywords = field.deconstruct()

    assert name == 'test_field'
    assert path == 'django.db.models.fields.__init__.TestField'
    assert args == []
    assert keywords['verbose_name'] == 'Test Field'
    assert keywords['max_length'] == 255
    assert keywords['unique'] is True
    assert 'db_index' not in keywords  # default value False