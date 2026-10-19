import pytest
from django.contrib.admin.filters import ListFilter
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class TestListFilter(ListFilter):
    def __init__(self, request=None, params=None, model=None, model_admin=None):
        super().__init__(request, params, model, model_admin)

    def has_output(self):
        return True

    def queryset(self, request, queryset):
        return queryset

    def expected_parameters(self):
        return {}

def test_choices_raises_not_implemented_error():
    filter_instance = TestListFilter()
    with pytest.raises(NotImplementedError):
        filter_instance.choices(None)

def test_choices_not_implemented_with_valid_params():
    filter_instance = TestListFilter(request=None, params={}, model=User, model_admin=None)
    with pytest.raises(NotImplementedError):
        filter_instance.choices(None)