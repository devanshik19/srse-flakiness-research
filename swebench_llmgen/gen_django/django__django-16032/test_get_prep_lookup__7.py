import warnings
import pytest
from django.contrib.auth.models import User
from django.db.models import ForeignKey
from django.db.models.fields.related_lookups import RelatedIn
from django.db.models.fields.related import MultiColSource
from django.utils.deprecation import RemovedInDjango50Warning


class MockTargetField:
    def get_prep_value(self, value):
        return str(value)


class MockOutputField:
    def __init__(self):
        self.path_infos = [[MockTargetField()]]


class MockLHS:
    def __init__(self):
        self.output_field = MockOutputField()
        self.field = ForeignKey(User, on_delete=None)


class MockRHS:
    def __init__(self):
        self.has_select_fields = True

    def clear_select_clause(self):
        pass

    def add_fields(self, fields, clear):
        pass


def test_get_prep_lookup_single_column_relations():
    lhs = MockLHS()
    rhs = MockRHS()
    lookup = RelatedIn()

    # Setting up mock attributes
    lookup.lhs = lhs
    lookup.rhs = [1, 2, '3']  # Some mixed values to normalize

    result = lookup.get_prep_lookup()
    
    assert result is not None
    assert lookup.rhs == ['1', '2', '3']  # Check normalized values


def test_get_prep_lookup_without_select_fields():
    lhs = MockLHS()
    rhs = MockRHS()
    rhs.has_select_fields = False  # Simulate non-select fields situation
    lookup = RelatedIn()

    # Setting up mock attributes
    lookup.lhs = lhs
    lookup.rhs = [1, 2, 3]

    result = lookup.get_prep_lookup()
    
    assert result is not None


def test_get_prep_lookup_primary_key_case():
    lhs = MockLHS()
    rhs = MockRHS()
    lookup = RelatedIn()

    # Setting up mock attributes
    lookup.lhs = lhs
    lookup.rhs = [1, 2, 3]
    lhs.output_field.primary_key = True  # Simulating the primary key case

    result = lookup.get_prep_lookup()

    assert result is not None
    # Add additional assertions based on the behavior expected in this scenario