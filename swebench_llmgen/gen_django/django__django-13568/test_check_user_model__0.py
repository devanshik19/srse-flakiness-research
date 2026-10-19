import pytest
from django.contrib.auth.models import User
from django.core import checks
from django.apps import apps
from django.conf import settings

def test_check_user_model_no_app_configs():
    settings.AUTH_USER_MODEL = 'auth.User'
    errors = check_user_model()
    assert errors == []

def test_check_user_model_with_invalid_required_fields():
    class CustomUserModel:
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = 'email'

        _meta = type('Meta', (), {
            'object_name': 'CustomUserModel',
            'get_field': lambda self, field: type('Field', (), {'unique': True})()
        })()

    apps.get_model = lambda app_label, model_name: CustomUserModel
    settings.AUTH_USER_MODEL = 'app_name.CustomUserModel'
    
    errors = check_user_model(app_configs=[apps.get_app_config('app_name')])
    assert len(errors) == 1
    assert errors[0] == checks.Error(
        "'REQUIRED_FIELDS' must be a list or tuple.",
        obj=CustomUserModel,
        id='auth.E001',
    )

def test_check_user_model_username_field_in_required_fields():
    class CustomUserModel:
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = ['username', 'email']

        _meta = type('Meta', (), {
            'object_name': 'CustomUserModel',
            'get_field': lambda self, field: type('Field', (), {'unique': True})()
        })()

    apps.get_model = lambda app_label, model_name: CustomUserModel
    settings.AUTH_USER_MODEL = 'app_name.CustomUserModel'
    
    errors = check_user_model(app_configs=[apps.get_app_config('app_name')])
    assert len(errors) == 1
    assert errors[0] == checks.Error(
        "The field named as the 'USERNAME_FIELD' "
        "for a custom user model must not be included in 'REQUIRED_FIELDS'.",
        hint="The 'USERNAME_FIELD' is currently set to 'username', you "
             "should remove 'username' from the 'REQUIRED_FIELDS'.",
        obj=CustomUserModel,
        id='auth.E002',
    )

def test_check_user_model_non_unique_username_field():
    class CustomUserModel:
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = []
        
        _meta = type('Meta', (), {
            'object_name': 'CustomUserModel',
            'get_field': lambda self, field: type('Field', (), {'unique': False})()
        })()

    apps.get_model = lambda app_label, model_name: CustomUserModel
    settings.AUTH_USER_MODEL = 'app_name.CustomUserModel'
    
    errors = check_user_model(app_configs=[apps.get_app_config('app_name')])
    assert len(errors) == 1
    assert errors[0] == checks.Error(
        "'%s.%s' must be unique because it is named as the 'USERNAME_FIELD'." % (
            CustomUserModel._meta.object_name, CustomUserModel.USERNAME_FIELD
        ),
        obj=CustomUserModel,
        id='auth.E003',
    )

def test_check_user_model_is_anonymous_method():
    class CustomUserModel:
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = []

        def is_anonymous(self):
            return True

        _meta = type('Meta', (), {
            'object_name': 'CustomUserModel',
            'get_field': lambda self, field: type('Field', (), {'unique': True})()
        })()
    
    apps.get_model = lambda app_label, model_name: CustomUserModel
    settings.AUTH_USER_MODEL = 'app_name.CustomUserModel'
    
    errors = check_user_model(app_configs=[apps.get_app_config('app_name')])
    assert len(errors) == 1
    assert errors[0] == checks.Critical(
        '%s.is_anonymous must be an attribute or property rather than '
        'a method. Ignoring this is a security issue as anonymous '
        'users will be treated as authenticated!' % CustomUserModel,
        obj=CustomUserModel,
        id='auth.C009',
    )

def test_check_user_model_is_authenticated_method():
    class CustomUserModel:
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = []

        def is_authenticated(self):
            return True

        _meta = type('Meta', (), {
            'object_name': 'CustomUserModel',
            'get_field': lambda self, field: type('Field', (), {'unique': True})()
        })()
    
    apps.get_model = lambda app_label, model_name: CustomUserModel
    settings.AUTH_USER_MODEL = 'app_name.CustomUserModel'
    
    errors = check_user_model(app_configs=[apps.get_app_config('app_name')])
    assert len(errors) == 1
    assert errors[0] == checks.Critical(
        '%s.is_authenticated must be an attribute or property rather '
        'than a method. Ignoring this is a security issue as anonymous '
        'users will be treated as authenticated!' % CustomUserModel,
        obj=CustomUserModel,
        id='auth.C010',
    )