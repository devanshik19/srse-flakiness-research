import pytest
from django.forms import BaseForm
from django.contrib.auth.models import User

class TestBaseForm(BaseForm):
    def __init__(self, data=None, files=None):
        super().__init__(data, files, auto_id=None, prefix=None, initial=None, 
                         error_class=None, label_suffix=None, empty_permitted=False,
                         field_order=None, use_required_attribute=False, renderer=None)

# Create a subclass for testing purpose
class TestForm(TestBaseForm):
    fields = ['username', 'email']

def test_repr_with_errors():
    form = TestForm(data={'username': '', 'email': ''})
    form._errors = {'username': [ValidationError(_('This field is required.'))]}
    form.is_bound = True
    expected_repr = '<TestForm bound=True, valid=False, fields=(username;email)>'
    assert repr(form) == expected_repr

def test_repr_without_errors():
    form = TestForm(data={'username': 'testuser', 'email': 'test@example.com'})
    form._errors = None
    form.is_bound = True
    expected_repr = '<TestForm bound=True, valid=Unknown, fields=(username;email)>'
    assert repr(form) == expected_repr

def test_repr_not_bound():
    form = TestForm()
    form.is_bound = False
    form._errors = None
    expected_repr = '<TestForm bound=False, valid=Unknown, fields=(username;email)>'
    assert repr(form) == expected_repr