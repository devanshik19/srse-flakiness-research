import pytest
import enum
from django.utils.functional import Promise

class ChoicesMeta:
    choices = [
        (1, 'Choice 1'),
        (2, 'Choice 2'),
        (3, 'Choice 3'),
    ]

    @classmethod
    def values(cls):
        return [value for value, _ in cls.choices]

    def __new__(metacls, classname, bases, classdict):
        return super().__new__(metacls, classname, bases, classdict)

    @classmethod
    def __contains__(cls, member):
        return member in [value for value, _ in cls.choices]

    @classmethod
    def names(cls):
        return [name for _, name in cls.choices]

    @classmethod
    def labels(cls):
        return [label for _, label in cls.choices]


def test_choices_meta_values():
    expected_values = [1, 2, 3]
    actual_values = ChoicesMeta.values()
    assert actual_values == expected_values