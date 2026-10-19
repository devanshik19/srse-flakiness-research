import pytest
from django.contrib.admin.filters import ListFilter
from django.contrib.auth.models import User

class TestListFilter(ListFilter):
    title = 'Test Filter'
    template = 'admin/filter_template.html'

    def has_output(self):
        return True  # Implementing the abstract method for testing

def test_has_output():
    filter_instance = TestListFilter(None, None, None, None)
    assert filter_instance.has_output() is True

def test_has_output_not_implemented():
    class NotImplementedListFilter(ListFilter):
        title = 'Not Implemented Filter'
        template = 'admin/filter_template.html'

    filter_instance = NotImplementedListFilter(None, None, None, None)
    
    with pytest.raises(NotImplementedError):
        filter_instance.has_output()