import pytest
from django.contrib.auth.models import User
from django.conf import settings
from django.core import checks
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from .checks import check_user_model

def test_check_user_model_requied_fields_not_list():
    User.REQUIRED_FIELDS = "not_a_list"
    errors = check_user_model()
    assert len(errors) == 1
    assert errors[0].msg == "'REQUIRED_FIELDS' must be a list or tuple."
    assert errors[0].id == 'auth.E001'

def test_check_user_model_username_field_in_required_fields():
    User.REQUIRED_FIELDS = [User.USERNAME_FIELD]
    errors = check_user_model()
    assert len(errors) == 1
    assert errors[0].msg == "The field named as the 'USERNAME_FIELD' for a custom user model must not be included in 'REQUIRED_FIELDS'."
    assert errors[0].id == 'auth.E002'

def test_check_user_model_username_field_not_unique():
    User._meta.get_field(User.USERNAME_FIELD).unique = False
    settings.AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
    errors = check_user_model()
    assert len(errors) == 1
    assert errors[0].msg == "'%s.%s' must be unique because it is named as the 'USERNAME_FIELD'." % (User._meta.object_name, User.USERNAME_FIELD)
    assert errors[0].id == 'auth.E003'

def test_check_user_model_username_field_not_unique_warning():
    User._meta.get_field(User.USERNAME_FIELD).unique = False
    settings.AUTHENTICATION_BACKENDS = ['another.backend']
    errors = check_user_model()
    assert len(errors) == 1
    assert errors[0].msg == "'%s.%s' is named as the 'USERNAME_FIELD', but it is not unique." % (User._meta.object_name, User.USERNAME_FIELD)
    assert errors[0].id == 'auth.W004'

def test_check_user_model_is_anonymous_method():
    def is_anonymous_method(self):
        return True
    User.is_anonymous = is_anonymous_method
    errors = check_user_model()
    assert len(errors) == 1
    assert errors[0].msg == '%s.is_anonymous must be an attribute or property rather than a method. Ignoring this is a security issue as anonymous users will be treated as authenticated!' % User
    assert errors[0].id == 'auth.C009'

def test_check_user_model_is_authenticated_method():
    def is_authenticated_method(self):
        return True
    User.is_authenticated = is_authenticated_method
    errors = check_user_model()
    assert len(errors) == 1
    assert errors[0].msg == '%s.is_authenticated must be an attribute or property rather than a method. Ignoring this is a security issue as anonymous users will be treated as authenticated!' % User
    assert errors[0].id == 'auth.C010'