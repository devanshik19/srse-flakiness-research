import pytest
from django.contrib.admin.filters import ListFilter
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class TestListFilter(ListFilter):
    title = 'Test Filter'
    template = 'test_template.html'

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)

    def has_output(self):
        return True

    def queryset(self, request, queryset):
        return queryset

    def expected_parameters(self):
        return {}

def test_choices_not_implemented():
    list_filter = TestListFilter(None, None, User, None)
    with pytest.raises(NotImplementedError, match='subclasses of ListFilter must provide a choices() method'):
        list_filter.choices(None)

def test_list_filter_initialization():
    list_filter = TestListFilter(None, None, User, None)
    assert list_filter.title == 'Test Filter'
    assert list_filter.template == 'test_template.html'
    assert list_filter.has_output() is True