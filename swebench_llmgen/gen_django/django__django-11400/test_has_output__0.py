import pytest
from django.contrib.admin.filters import ListFilter
from django.contrib.auth.models import User

class TestListFilter(ListFilter):
    def has_output(self):
        return True  # Example implementation for testing

def test_has_output():
    list_filter = TestListFilter(request=None, params={}, model=User, model_admin=None)

    # Test that the method returns True
    assert list_filter.has_output() is True

def test_has_output_not_implemented():
    class NotImplementedListFilter(ListFilter):
        pass

    not_impl_filter = NotImplementedListFilter(request=None, params={}, model=User, model_admin=None)

    # Test that calling has_output raises NotImplementedError
    with pytest.raises(NotImplementedError, match='subclasses of ListFilter must provide a has_output() method'):
        not_impl_filter.has_output()