import collections.abc
import datetime
import pytest
from django.contrib.auth.models import User
from django.db.models import CharField

class TestFieldDeconstruct:
    
    @pytest.fixture
    def field(self):
        return CharField(max_length=100, null=True, default='test', blank=True)

    def test_deconstruct_returns_correct_tuple(self, field):
        # Arrange
        field.name = 'test_field'
        expected_path = 'django.db.models.fields.char.CharField'
        expected_keywords = {
            'max_length': 100,
            'null': True,
            'default': 'test',
            'blank': True,
        }

        # Act
        result = field.deconstruct()

        # Assert
        assert result[0] == field.name
        assert result[1] == expected_path
        assert result[2] == []  # No positional arguments
        assert all(item in result[3].items() for item in expected_keywords.items())

    def test_deconstruct_excludes_default_values(self, field):
        # Arrange
        field.name = 'another_field'
        field.verbose_name = 'Another Field'
        field.primary_key = False
        field.default = 'default_value'

        expected_keywords = {
            'verbose_name': 'Another Field',
            'default': 'default_value',
        }

        # Act
        result = field.deconstruct()

        # Assert
        assert result[3] == expected_keywords

    def test_deconstruct_includes_choices(self, field):
        # Arrange
        field.choices = [('option1', 'Option 1'), ('option2', 'Option 2')]
        field.name = 'choice_field'
        
        expected_keywords = {
            'choices': list(field.choices)
        }

        # Act
        result = field.deconstruct()

        # Assert
        assert result[3]['choices'] == expected_keywords['choices']

    def test_deconstruct_with_empty_choices(self, field):
        # Arrange
        field.choices = []
        field.name = 'empty_choice_field'
        
        expected_keywords = {
            'choices': []
        }

        # Act
        result = field.deconstruct()

        # Assert
        assert result[3]['choices'] == expected_keywords['choices']