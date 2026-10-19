import pytest
from django.contrib.admin.filters import ListFilter

class TestListFilter(ListFilter):
    def has_output(self):
        return True

def test_has_output():
    filter_instance = TestListFilter(None, None, None, None)
    assert filter_instance.has_output() is True

def test_has_output_not_implemented():
    class IncompleteListFilter(ListFilter):
        pass

    filter_instance = IncompleteListFilter(None, None, None, None)
    with pytest.raises(NotImplementedError):
        filter_instance.has_output()