import pytest
from django.contrib.admin import ListFilter
from django.contrib.auth.models import User


class TestListFilter(ListFilter):
    def has_output(self):
        return False


def test_list_filter_has_output_not_implemented():
    filter_instance = ListFilter(request=None, params={}, model=User, model_admin=None)
    with pytest.raises(NotImplementedError, match='subclasses of ListFilter must provide a has_output() method'):
        filter_instance.has_output()


def test_test_list_filter_has_output():
    filter_instance = TestListFilter(request=None, params={}, model=User, model_admin=None)
    assert filter_instance.has_output() is False