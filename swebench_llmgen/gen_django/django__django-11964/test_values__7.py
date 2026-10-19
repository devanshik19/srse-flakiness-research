import pytest
from django.contrib.auth.models import User
from django.db import models


class ChoicesMeta:
    choices = [
        (1, 'Choice 1'),
        (2, 'Choice 2'),
        (3, 'Choice 3')
    ]

    @classmethod
    def values(cls):
        return [value for value, _ in cls.choices]


def test_values_method():
    # Test that the values method returns the correct list
    expected_values = [1, 2, 3]
    actual_values = ChoicesMeta.values()
    assert actual_values == expected_values

    # Test that the order of values is correct
    assert actual_values[0] == 1
    assert actual_values[1] == 2
    assert actual_values[2] == 3

    # Test that the method returns a list
    assert isinstance(actual_values, list)