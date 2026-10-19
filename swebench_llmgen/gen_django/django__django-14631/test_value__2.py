import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestBoundField:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='testpass')

    @pytest.fixture
    def form(self, user):
        class TestForm(forms.Form):
            username = forms.CharField(initial='default_user')
        
        return TestForm(initial={'username': user.username})

    @pytest.fixture
    def bound_field(self, form):
        return BoundField(form, form.fields['username'], 'username')

    def test_value_initial(self, bound_field):
        assert bound_field.value() == 'default_user'

    def test_value_bound(self, bound_field, user):
        # Bind the form with data
        bound_field.form.data = {'username': 'new_user'}
        bound_field.form.is_bound = True
        assert bound_field.value() == 'new_user'

    def test_value_bound_with_initial(self, bound_field, user):
        # Test when initial value is overridden despite being bound
        bound_field.form.data = {'username': ''}
        bound_field.form.is_bound = True
        assert bound_field.value() == ''  # Should return empty because data is empty

    def test_value_when_not_bound(self, bound_field):
        # Check the behavior when the form is not bound
        bound_field.form.is_bound = False
        assert bound_field.value() == 'default_user'