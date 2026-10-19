import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestBoundFieldData:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='password')

    @pytest.fixture
    def form(self, user):
        class TestForm(forms.Form):
            username = forms.CharField()
            password = forms.CharField(widget=forms.PasswordInput)

        return TestForm(initial={'username': user.username, 'password': 'password'})

    @pytest.fixture
    def bound_field(self, form):
        return BoundField(form, form.fields['username'], 'username')

    def test_data_return_value(self, bound_field):
        assert bound_field.data() == 'testuser'

    def test_data_with_empty_initial(self, form):
        form.fields['username'].initial = ''
        bound_field = BoundField(form, form.fields['username'], 'username')
        assert bound_field.data() is None

    def test_data_with_no_initial_value(self, form):
        form.fields['username'].initial = None
        bound_field = BoundField(form, form.fields['username'], 'username')
        assert bound_field.data() is None