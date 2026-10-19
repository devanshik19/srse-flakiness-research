import collections.abc
from django.db import models
from django.contrib.auth.models import User
import pytest

class CustomField(models.Field):
    def __init__(self, name='custom_field', verbose_name=None, **kwargs):
        self.name = name
        self.verbose_name = verbose_name
        super().__init__(**kwargs)

@pytest.fixture
def custom_field():
    return CustomField()

def test_deconstruct_with_no_overrides(custom_field):
    custom_field.name = 'test_field'
    custom_field.verbose_name = 'Test Field'
    
    expected = (
        'test_field',
        'django.db.models.fields.Field',  # Adjusted import path for the sake of this test
        [],
        {
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
    )

    assert custom_field.deconstruct() == expected

def test_deconstruct_with_choices(custom_field):
    custom_field.name = 'test_field_with_choices'
    custom_field.choices = [('1', 'One'), ('2', 'Two')]
    
    expected_keywords = {
        'verbose_name': None,
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
        'choices': [('1', 'One'), ('2', 'Two')],
        'help_text': '',
        'db_column': None,
        'db_tablespace': None,
        'auto_created': False,
        'validators': [],
        'error_messages': None,
    }

    result_name, result_path, result_args, result_keywords = custom_field.deconstruct()
    
    assert result_name == 'test_field_with_choices'
    assert result_path.startswith('django.db.models.fields')
    assert result_args == []
    assert result_keywords == expected_keywords

def test_deconstruct_with_custom_value(custom_field):
    custom_field.name = 'custom_field_example'
    custom_field.default = 'default_value'
    
    expected_keywords = {
        'verbose_name': None,
        'primary_key': False,
        'max_length': None,
        'unique': False,
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
        'validators': [],
        'error_messages': None,
    }

    result_name, result_path, result_args, result_keywords = custom_field.deconstruct()
    
    assert result_name == 'custom_field_example'
    assert result_path.startswith('django.db.models.fields')
    assert result_args == []
    assert result_keywords == expected_keywords