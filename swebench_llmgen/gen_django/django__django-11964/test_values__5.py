import pytest
from django.db import models
import enum

class ChoicesMeta:
    choices = []

    def __new__(metacls, classname, bases, classdict):
        return super().__new__(metacls, classname, bases, classdict)

    @classmethod
    def __contains__(cls, member):
        return member in dict(cls.choices)

    @classmethod
    def names(cls):
        return [name for _, name in cls.choices]

    @classmethod
    def choices(cls):
        return cls.choices

    @classmethod
    def labels(cls):
        return [label for _, label in cls.choices]

    @classmethod
    def values(cls):
        return [value for value, _ in cls.choices]


class TestChoicesEnum(enum.Enum):
    OPTION_1 = 'value1', 'Label 1'
    OPTION_2 = 'value2', 'Label 2'

ChoicesMeta.choices = TestChoicesEnum.choices()

def test_values():
    expected_values = ['value1', 'value2']
    assert ChoicesMeta.values() == expected_values

def test_choices():
    assert ChoicesMeta.choices() == TestChoicesEnum.choices()

def test_contains():
    assert 'value1' in ChoicesMeta
    assert 'value3' not in ChoicesMeta

def test_names():
    expected_names = ['Label 1', 'Label 2']
    assert ChoicesMeta.names() == expected_names

def test_labels():
    expected_labels = ['Label 1', 'Label 2']
    assert ChoicesMeta.labels() == expected_labels