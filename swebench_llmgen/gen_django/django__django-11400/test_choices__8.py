import pytest
from django.contrib.admin.filters import ListFilter
from django.contrib.auth.models import User


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


def test_choices_raises_not_implemented_error():
    request = None
    params = {}
    model = User
    model_admin = None  # Assuming we don't need a real ModelAdmin for this test

    test_filter = TestListFilter(request, params, model, model_admin)

    with pytest.raises(NotImplementedError, match='subclasses of ListFilter must provide a choices() method'):
        test_filter.choices(None)