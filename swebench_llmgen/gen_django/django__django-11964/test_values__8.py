import pytest
from django.db.models.enums import ChoicesMeta

class TestChoicesMeta(ChoicesMeta):

    choices = (
        (1, 'Choice One'),
        (2, 'Choice Two'),
        (3, 'Choice Three'),
    )

def test_values():
    expected_values = [1, 2, 3]
    actual_values = TestChoicesMeta.values()
    assert actual_values == expected_values