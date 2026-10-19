import pytest
from django.contrib.admin.filters import ListFilter
from django.contrib.auth.models import User

class SimpleListFilter(ListFilter):
    def has_output(self):
        return True  # A concrete implementation for testing

def test_has_output():
    filter_instance = SimpleListFilter(None, {}, User, None)
    assert filter_instance.has_output() is True

    # Testing if NotImplementedError is raised when using the base class
    with pytest.raises(NotImplementedError):
        base_filter = ListFilter(None, {}, User, None)
        base_filter.has_output()