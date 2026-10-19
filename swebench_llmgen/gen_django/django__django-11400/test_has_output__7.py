import pytest
from django.contrib.admin.filters import ListFilter
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured, ValidationError

class TestListFilter(ListFilter):
    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)

    def has_output(self):
        raise NotImplementedError('subclasses of ListFilter must provide a has_output() method')

def test_list_filter_has_output_not_implemented():
    filter_instance = TestListFilter(request=None, params=None, model=User, model_admin=None)

    with pytest.raises(NotImplementedError, match='subclasses of ListFilter must provide a has_output() method'):
        filter_instance.has_output()