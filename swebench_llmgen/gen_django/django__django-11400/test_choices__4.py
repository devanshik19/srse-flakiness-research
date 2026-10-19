import pytest
from django.contrib.admin.filters import ListFilter
from django.contrib.auth.models import User
from django.contrib.admin.utils import IncorrectLookupParameters

class MockChangeList:
    def __init__(self, model):
        self.model = model

class TestListFilter(ListFilter):
    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)

    def choices(self, changelist):
        super().choices(changelist)

def test_choices_not_implemented():
    changelist = MockChangeList(User)
    filter_instance = TestListFilter(None, {}, User, None)
    
    with pytest.raises(NotImplementedError) as excinfo:
        filter_instance.choices(changelist)
    
    assert str(excinfo.value) == 'subclasses of ListFilter must provide a choices() method'