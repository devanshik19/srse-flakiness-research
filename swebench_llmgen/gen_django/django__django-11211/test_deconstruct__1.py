import collections.abc
from django.db import models
from django.contrib.auth.models import User
import pytest

class TestField(models.Field):
    def __init__(self, name, **kwargs):
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__()

def test_deconstruct():
    field = TestField(
        name='my_field',
        verbose_name='My Field',
        primary_key=True,
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        db_index=True,
        default='default_value',
        editable=False,
        serialize=False,
        unique_for_date=None,
        unique_for_month=None,
        unique_for_year=None,
        choices=[(1, 'Choice 1'), (2, 'Choice 2')],
        help_text='Help text here',
        db_column='my_field_db',
        db_tablespace='my_tablespace',
        auto_created=True,
        validators=[],
        error_messages=None,
    )

    name, path, args, kwargs = field.deconstruct()

    assert name == 'my_field'
    assert path == 'path.to.TestField'
    assert args == []
    assert kwargs == {
        'verbose_name': 'My Field',
        'primary_key': True,
        'max_length': 100,
        'unique': True,
        'blank': False,
        'null': False,
        'db_index': True,
        'default': 'default_value',
        'editable': False,
        'serialize': False,
        'unique_for_date': None,
        'unique_for_month': None,
        'unique_for_year': None,
        'choices': [(1, 'Choice 1'), (2, 'Choice 2')],
        'help_text': 'Help text here',
        'db_column': 'my_field_db',
        'db_tablespace': 'my_tablespace',
        'auto_created': True,
        'validators': [],
        'error_messages': None,
    }