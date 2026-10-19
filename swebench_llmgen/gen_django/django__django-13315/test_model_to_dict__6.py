import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

@pytest.mark.parametrize("fields, exclude, expected", [
    (None, None, {'username': 'testuser', 'email': 'testuser@example.com'}),
    (['username'], None, {'username': 'testuser'}),
    (None, ['email'], {'username': 'testuser'}),
    (['username', 'email'], ['email'], {'username': 'testuser'}),
])
def test_model_to_dict(fields, exclude, expected):
    user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password')

    result = model_to_dict(user, fields=fields, exclude=exclude)

    assert result == expected

def test_model_to_dict_empty_fields():
    user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password')

    result = model_to_dict(user, fields=[], exclude=[])

    assert result == {}

def test_model_to_dict_individual_fields():
    user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password')

    result = model_to_dict(user, fields=['username', 'first_name'], exclude=[])

    assert 'first_name' not in result
    assert result['username'] == 'testuser'