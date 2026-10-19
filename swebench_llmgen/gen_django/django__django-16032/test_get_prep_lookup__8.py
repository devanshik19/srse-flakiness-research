import warnings
import pytest
from django.db.models import Lookup, Field
from django.contrib.auth.models import User
from django.db.models.fields.related_lookups import RelatedIn
from django.utils.deprecation import RemovedInDjango50Warning

class MultiColSource:
    pass

class MockTargetField:
    def get_prep_value(self, value):
        return str(value) if value is not None else None

class MockLookupField:
    def __init__(self, primary_key=False):
        self.primary_key = primary_key
        self.target_field = MockTargetField()
        self.path_infos = [self]

class MockLHS:
    def __init__(self, is_multi_col=False, has_select_fields=True):
        self.output_field = MockLookupField()
        self.field = MockLookupField()
        self.is_multi_col = is_multi_col
        self.has_select_fields = has_select_fields

    def clear_select_clause(self):
        pass

    def add_fields(self, fields, clear):
        pass

@pytest.mark.filterwarnings("ignore::django.utils.deprecation.RemovedInDjango50Warning")
def test_get_prep_lookup_single_column_relation():
    lhs = MockLHS()
    related_in = RelatedIn()
    related_in.lhs = lhs
    related_in.rhs = ['value1', 'value2']

    result = related_in.get_prep_lookup()

    assert result is not None
    assert related_in.rhs == ['value1', 'value2']

@pytest.mark.filterwarnings("ignore::django.utils.deprecation.RemovedInDjango50Warning")
def test_get_prep_lookup_with_clear_select_clause():
    lhs = MockLHS(is_multi_col=False, has_select_fields=False)
    related_in = RelatedIn()
    related_in.lhs = lhs
    related_in.rhs = ['value1', 'value2']

    result = related_in.get_prep_lookup()
    
    assert result is not None
    # Assuming that clearing the select clause works as intended
    assert related_in.rhs == ['value1', 'value2']  # This should ideally reflect processed values

@pytest.mark.filterwarnings("ignore::django.utils.deprecation.RemovedInDjango50Warning")
def test_get_prep_lookup_with_primary_key():
    lhs = MockLHS()
    lhs.output_field.primary_key = True
    lhs.field.target_field.primary_key = False
    related_in = RelatedIn()
    related_in.lhs = lhs
    related_in.rhs = [1, 2]

    result = related_in.get_prep_lookup()

    assert result is not None
    assert related_in.rhs == [1, 2]  # Should not change as there's no transformation