import enum
import pytest
from django.utils.functional import Promise

class ChoicesMeta:
    choices = [
        ('value1', 'Label 1'),
        ('value2', 'Label 2'),
        ('value3', 'Label 3')
    ]

    @classmethod
    def values(cls):
        return [value for value, _ in cls.choices]

    @classmethod
    def __new__(metacls, classname, bases, classdict):
        return super().__new__(metacls, classname, bases)

    @classmethod
    def __contains__(cls, member):
        return any(value == member for value, _ in cls.choices)

    @classmethod
    def names(cls):
        return [name for _, name in cls.choices]

    @classmethod
    def labels(cls):
        return [label for _, label in cls.choices]

@pytest.mark.parametrize("expected_values", [
    (['value1', 'value2', 'value3']),
])
def test_values(expected_values):
    assert ChoicesMeta.values() == expected_values