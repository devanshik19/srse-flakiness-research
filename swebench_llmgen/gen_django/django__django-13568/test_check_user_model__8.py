import pytest
from django.contrib.auth import get_user_model
from django.core import checks
from django.conf import settings
from django.apps import apps

from django.contrib.auth.checks import check_user_model

@pytest.mark.parametrize('app_configs, expected_errors', [
    (None, []),  # Case when no app_configs are provided
    ([apps.get_app_config('auth')], []),  # Correct user model case with no issues
])
def test_check_user_model_valid(app_configs, expected_errors):
    errors = check_user_model(app_configs)
    assert errors == expected_errors


def test_check_user_model_required_fields_not_list():
    User = get_user_model()
    User.REQUIRED_FIELDS = 'not_a_list'
    errors = check_user_model([apps.get_app_config('auth')])
    assert len(errors) == 1
    assert errors[0].id == 'auth.E001'


def test_check_user_model_username_field_in_required_fields():
    User = get_user_model()
    User.REQUIRED_FIELDS = [User.USERNAME_FIELD]
    errors = check_user_model([apps.get_app_config('auth')])
    assert len(errors) == 1
    assert errors[0].id == 'auth.E002'


def test_check_user_model_username_field_not_unique():
    User = get_user_model()
    User._meta.get_field(User.USERNAME_FIELD).unique = False
    settings.AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
    errors = check_user_model([apps.get_app_config('auth')])
    assert len(errors) == 1
    assert errors[0].id == 'auth.E003'


def test_check_user_model_username_field_warning_on_non_unique():
    User = get_user_model()
    User._meta.get_field(User.USERNAME_FIELD).unique = False
    settings.AUTHENTICATION_BACKENDS = ['some.other.Backend']
    errors = check_user_model([apps.get_app_config('auth')])
    assert len(errors) == 1
    assert errors[0].id == 'auth.W004'


def test_check_user_model_is_anonymous_method():
    User = get_user_model()
    User.is_anonymous = lambda self: True
    errors = check_user_model([apps.get_app_config('auth')])
    assert len(errors) == 1
    assert errors[0].id == 'auth.C009'


def test_check_user_model_is_authenticated_method():
    User = get_user_model()
    User.is_authenticated = lambda self: True
    errors = check_user_model([apps.get_app_config('auth')])
    assert len(errors) == 1
    assert errors[0].id == 'auth.C010'