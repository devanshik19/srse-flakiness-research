import enum
import pytest
from django.utils.functional import Promise

class ChoicesMeta(enum.EnumMeta):
    choices = (
        ('choice1', 'Choice 1'),
        ('choice2', 'Choice 2'),
    )

    def __new__(metacls, classname, bases, classdict):
        return super().__new__(metacls, classname, bases, classdict)

    def __contains__(cls, member):
        return member in cls.choices

    def names(cls):
        return [name for name, _ in cls.choices]

    def choices(cls):
        return cls.choices

    def labels(cls):
        return [label for _, label in cls.choices]

    def values(cls):
        return [value for value, _ in cls.choices]

class Choices(enum.Enum, metaclass=ChoicesMeta):
    pass

def test_values():
    assert Choices.values() == ['choice1', 'choice2']