import pytest
import enum
from django.utils.functional import Promise

class ChoicesMeta:
    choices = [
        ('value1', 'Label 1'),
        ('value2', 'Label 2')
    ]

    @classmethod
    def values(cls):
        return [value for value, _ in cls.choices]

class TestChoicesMeta:

    def test_values(self):
        expected_values = ['value1', 'value2']
        assert ChoicesMeta.values() == expected_values

    def test_values_empty(self):
        ChoicesMeta.choices = []
        assert ChoicesMeta.values() == []