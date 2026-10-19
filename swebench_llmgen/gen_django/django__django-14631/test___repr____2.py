import pytest
from django import forms
from django.contrib.auth.models import User

class TestBaseForm:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_repr_bound_valid(self):
        form_data = {'username': 'testuser', 'password': 'testpass'}
        form = forms.Form(data=form_data)
        form.is_bound = True
        form._errors = {}

        assert repr(form) == '<Form bound=True, valid=True, fields=(username;password)>'

    def test_repr_bound_invalid(self):
        form_data = {'username': '', 'password': ''}
        form = forms.Form(data=form_data)
        form.is_bound = True
        form._errors = {'username': ['This field is required.'], 'password': ['This field is required.']}

        assert repr(form) == '<Form bound=True, valid=False, fields=(username;password)>'

    def test_repr_unbound(self):
        form = forms.Form(data=None)
        form.is_bound = False
        form._errors = None

        assert repr(form) == '<Form bound=False, valid=Unknown, fields=(username;password)>'