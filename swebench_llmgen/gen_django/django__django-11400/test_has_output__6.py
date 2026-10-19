import pytest
from django.contrib.admin.filters import ListFilter
from django.contrib.auth.models import User

class TestListFilter(ListFilter):
    def has_output(self):
        return False  # Simple implementation to allow testing

def test_list_filter_has_output_not_implemented():
    with pytest.raises(NotImplementedError, match='subclasses of ListFilter must provide a has_output() method'):
        ListFilter(None, None, None, None)

def test_test_list_filter_has_output():
    test_filter = TestListFilter(None, None, User, None)
    assert test_filter.has_output() is False