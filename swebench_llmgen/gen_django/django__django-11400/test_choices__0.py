import datetime
import pytest
from django.contrib.admin.filters import ListFilter
from django.contrib.auth.models import User

class TestListFilter(ListFilter):

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        self.title = "Test Filter"
        self.template = "admin/test_filter.html"

    def has_output(self):
        return True

    def queryset(self, request, queryset):
        return queryset

    def expected_parameters(self):
        return {}

def test_choices_not_implemented():
    list_filter = TestListFilter(None, {}, User, None)
    with pytest.raises(NotImplementedError, match='subclasses of ListFilter must provide a choices() method'):
        list_filter.choices(None)