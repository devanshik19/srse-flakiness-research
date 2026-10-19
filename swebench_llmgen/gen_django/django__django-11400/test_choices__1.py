import pytest
from django.contrib.admin.filters import ListFilter
from django.contrib.auth.models import User
from django.contrib.admin.views.main import ChangeList

class TestListFilter(ListFilter):
    title = "Test Filter"
    template = "admin/test_filter.html"

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)

    def has_output(self):
        return True

    def queryset(self, request, queryset):
        return queryset

    def expected_parameters(self):
        return {}

def test_choices_not_implemented():
    with pytest.raises(NotImplementedError, match='subclasses of ListFilter must provide a choices() method'):
        filter_instance = TestListFilter(None, None, User, None)
        filter_instance.choices(ChangeList(None, None, None, None, None, None, None, None, None, None, None))