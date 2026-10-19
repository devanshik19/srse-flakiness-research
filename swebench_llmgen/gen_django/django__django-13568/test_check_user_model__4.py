import pytest
from django.contrib.auth.models import User
from django.core import checks
from django.conf import settings
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.checks import Error, Warning, Critical

def test_check_user_model_no_app_configs():
    errors = check_user_model()
    assert errors == []

def test_check_user_model_invalid_required_fields():
    class InvalidUserModel:
        AUTH_USER_MODEL = 'app.InvalidUser'
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = "email"

        class _meta:
            object_name = 'InvalidUser'

    apps.get_model = lambda app_label, model_name: InvalidUserModel
    settings.AUTH_USER_MODEL = 'app.InvalidUser'
    
    errors = check_user_model()
    assert len(errors) == 1
    assert isinstance(errors[0], Error)
    assert errors[0].id == 'auth.E001'

def test_check_user_model_username_field_in_required_fields():
    class InvalidUserModel:
        AUTH_USER_MODEL = 'app.InvalidUser'
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = ['username', 'email']

        class _meta:
            object_name = 'InvalidUser'

    apps.get_model = lambda app_label, model_name: InvalidUserModel
    settings.AUTH_USER_MODEL = 'app.InvalidUser'

    errors = check_user_model()
    assert len(errors) == 1
    assert isinstance(errors[0], Error)
    assert errors[0].id == 'auth.E002'

def test_check_user_model_username_field_not_unique():
    class UserModel:
        AUTH_USER_MODEL = 'app.UserModel'
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = []

        class _meta:
            object_name = 'UserModel'

        @classmethod
        def get_field(cls, field_name):
            class Field:
                unique = False
            return Field()

    apps.get_model = lambda app_label, model_name: UserModel
    settings.AUTH_USER_MODEL = 'app.UserModel'
    settings.AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

    errors = check_user_model()
    assert len(errors) == 1
    assert isinstance(errors[0], Error)
    assert errors[0].id == 'auth.E003'

def test_check_user_model_username_field_not_unique_warning():
    class UserModel:
        AUTH_USER_MODEL = 'app.UserModel'
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = []

        class _meta:
            object_name = 'UserModel'

        @classmethod
        def get_field(cls, field_name):
            class Field:
                unique = False
            return Field()

    apps.get_model = lambda app_label, model_name: UserModel
    settings.AUTH_USER_MODEL = 'app.UserModel'
    settings.AUTHENTICATION_BACKENDS = ['some.other.backend']

    errors = check_user_model()
    assert len(errors) == 1
    assert isinstance(errors[0], Warning)
    assert errors[0].id == 'auth.W004'

def test_check_user_model_is_anonymous_method():
    class InvalidUserModel:
        AUTH_USER_MODEL = 'app.InvalidUser'
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = []

        class _meta:
            object_name = 'InvalidUser'

        def is_anonymous(self):
            return False

    apps.get_model = lambda app_label, model_name: InvalidUserModel
    settings.AUTH_USER_MODEL = 'app.InvalidUser'
    
    errors = check_user_model()
    assert len(errors) == 1
    assert isinstance(errors[0], Critical)
    assert errors[0].id == 'auth.C009'

def test_check_user_model_is_authenticated_method():
    class InvalidUserModel:
        AUTH_USER_MODEL = 'app.InvalidUser'
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = []

        class _meta:
            object_name = 'InvalidUser'

        def is_authenticated(self):
            return True

    apps.get_model = lambda app_label, model_name: InvalidUserModel
    settings.AUTH_USER_MODEL = 'app.InvalidUser'
    
    errors = check_user_model()
    assert len(errors) == 1
    assert isinstance(errors[0], Critical)
    assert errors[0].id == 'auth.C010'