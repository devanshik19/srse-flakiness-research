import collections.abc
from django.db import models
from django.contrib.auth.models import User
import pytest


class CustomField(models.Field):
    def __init__(self, verbose_name=None, name=None, primary_key=False, **kwargs):
        super().__init__(verbose_name, name, primary_key, **kwargs)


def test_deconstruct():
    field = CustomField(
        verbose_name="Test Field",
        primary_key=True,
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        db_index=True,
        default="default_value",
        editable=True,
        serialize=True,
        choices=[(1, 'Choice 1'), (2, 'Choice 2')],
        help_text='Help text for custom field',
    )
    field.name = 'custom_field'
    
    # Calling deconstruct
    name, path, args, kwargs = field.deconstruct()

    # Assertions to check the deconstructed values
    assert name == 'custom_field'
    assert path == 'django.db.models.fields.__init__.CustomField'
    assert args == []
    assert kwargs['verbose_name'] == 'Test Field'
    assert kwargs['primary_key'] is True
    assert kwargs['max_length'] == 100
    assert kwargs['unique'] is True
    assert kwargs['blank'] is False
    assert kwargs['null'] is False
    assert kwargs['db_index'] is True
    assert kwargs['default'] == 'default_value'
    assert kwargs['editable'] is True
    assert kwargs['serialize'] is True
    assert kwargs['choices'] == [(1, 'Choice 1'), (2, 'Choice 2')]
    assert kwargs['help_text'] == 'Help text for custom field'