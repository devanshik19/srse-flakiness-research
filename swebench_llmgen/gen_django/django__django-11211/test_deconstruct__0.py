import collections.abc
import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User
import pytest

class TestField(models.Field):
    def __init__(self, name, **kwargs):
        self.name = name
        super().__init__(**kwargs)

def test_deconstruct_default_values():
    field = TestField(name='test_field', verbose_name='Test Field')

    name, path, args, keywords = field.deconstruct()

    assert name == 'test_field'
    assert path == 'django.db.models.fields.tests.TestField'
    assert args == []
    assert keywords == {
        'verbose_name': 'Test Field',
        'primary_key': False,
        'max_length': None,
        'unique': False,
        'blank': False,
        'null': False,
        'db_index': False,
        'default': models.NOT_PROVIDED,
        'editable': True,
        'serialize': True,
        'unique_for_date': None,
        'unique_for_month': None,
        'unique_for_year': None,
        'choices': None,
        'help_text': '',
        'db_column': None,
        'db_tablespace': None,
        'auto_created': False,
        'validators': [],
        'error_messages': None,
    }

def test_deconstruct_custom_values():
    field = TestField(
        name='another_test_field',
        verbose_name='Another Test Field',
        max_length=100,
        unique=True,
        default='default_value',
        validators=[validators.MinLengthValidator(5)],
    )

    name, path, args, keywords = field.deconstruct()

    assert name == 'another_test_field'
    assert path == 'django.db.models.fields.tests.TestField'
    assert args == []
    assert keywords == {
        'verbose_name': 'Another Test Field',
        'primary_key': False,
        'max_length': 100,
        'unique': True,
        'blank': False,
        'null': False,
        'db_index': False,
        'default': 'default_value',
        'editable': True,
        'serialize': True,
        'unique_for_date': None,
        'unique_for_month': None,
        'unique_for_year': None,
        'choices': None,
        'help_text': '',
        'db_column': None,
        'db_tablespace': None,
        'auto_created': False,
        'validators': [{'type': 'MinLengthValidator', 'args': [5]}],
        'error_messages': None,
    }

def test_deconstruct_choices():
    field = TestField(
        name='choice_field',
        choices=[(1, 'One'), (2, 'Two')]
    )

    name, path, args, keywords = field.deconstruct()

    assert name == 'choice_field'
    assert path == 'django.db.models.fields.tests.TestField'
    assert args == []
    assert 'choices' in keywords
    assert keywords['choices'] == [(1, 'One'), (2, 'Two')]