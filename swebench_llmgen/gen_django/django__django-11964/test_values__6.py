import enum
import pytest
from django.contrib.auth.models import User

class ChoicesMeta(enum.Enum):
    OPTION_ONE = 'option_one', 'Option One'
    OPTION_TWO = 'option_two', 'Option Two'

    @classmethod
    def values(cls):
        return [value for value, _ in cls.choices]

    @classmethod
    def choices(cls):
        return cls._value2member_map_.items()

def test_choices_meta_values():
    assert ChoicesMeta.values() == ['option_one', 'option_two']

def test_choices_meta_values_empty():
    class EmptyChoicesMeta(enum.Enum):
        @classmethod
        def choices(cls):
            return []

        @classmethod
        def values(cls):
            return [value for value, _ in cls.choices()]

    assert EmptyChoicesMeta.values() == []