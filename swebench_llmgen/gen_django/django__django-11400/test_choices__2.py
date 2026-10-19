import datetime
import pytest
from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.auth.models import User
from django.contrib.admin.filters import ListFilter

class TestListFilter(ListFilter):
    def __init__(self, request, params, model, model_admin):
        self.title = "Test Filter"
        self.template = "admin/filter_template.html"
        super().__init__(request, params, model, model_admin)

    def has_output(self):
        return True

    def expected_parameters(self):
        return []

    def queryset(self, request, queryset):
        return queryset

def test_choices_raises_notimplementederror():
    list_filter = TestListFilter(request=None, params={}, model=User, model_admin=None)
    
    with pytest.raises(NotImplementedError, match='subclasses of ListFilter must provide a choices() method'):
        list_filter.choices(changelist=None)