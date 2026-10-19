import pytest
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

@pytest.mark.parametrize(
    "fields, exclude, expected_result",
    [
        (None, None, {'username': 'testuser', 'email': 'testuser@example.com'}),
        (['username'], None, {'username': 'testuser'}),
        (None, ['email'], {'username': 'testuser'}),
        (['username', 'email'], ['email'], {'username': 'testuser'}),
    ]
)
def test_model_to_dict(fields, exclude, expected_result):
    user = User.objects.create(username='testuser', email='testuser@example.com')
    
    result = model_to_dict(user, fields=fields, exclude=exclude)
    
    assert result == expected_result