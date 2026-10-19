import pytest
from django.contrib.auth.models import User
from django.db.models.enums import ChoicesMeta

class TestChoicesMeta(ChoicesMeta):
    choices = [
        ('choice_one', 'Choice One'),
        ('choice_two', 'Choice Two'),
        ('choice_three', 'Choice Three')
    ]

def test_values():
    expected_values = ['choice_one', 'choice_two', 'choice_three']
    assert TestChoicesMeta.values() == expected_values