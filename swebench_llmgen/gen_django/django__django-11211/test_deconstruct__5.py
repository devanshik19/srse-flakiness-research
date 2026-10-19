import collections.abc
import pytest
from django.db import models

class TestField(models.Field):
    def __init__(self, name="test_field", **kwargs):
        super().__init__(verbose_name="Test Field", name=name, **kwargs)

def test_deconstruct():
    field = TestField(primary_key=True, max_length=100, unique=True, default='test', blank=True, choices=[('1', 'One'), ('2', 'Two')])
    
    name, path, args, keywords = field.deconstruct()
    
    assert name == 'test_field'
    assert path == 'django.db.models.fields.testfields.TestField'  # Adjust based on the actual path
    assert args == []
    
    expected_keywords = {
        'primary_key': True,
        'max_length': 100,
        'unique': True,
        'default': 'test',
        'blank': True,
        'choices': [('1', 'One'), ('2', 'Two')]
    }

    assert keywords == expected_keywords