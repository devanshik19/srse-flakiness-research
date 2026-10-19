import pytest
from django.contrib.auth.models import User
from django.apps import apps
from django.conf import settings
from django.core import checks
from django.contrib.auth.checks import check_user_model

@pytest.fixture
def set_auth_user_model():
    settings.AUTH_USER_MODEL = 'auth.User'

def test_check_user_model_with_default_user_model(set_auth_user_model):
    errors = check_user_model()
    
    assert len(errors) == 0

def test_check_user_model_with_custom_fields(set_auth_user_model):
    class CustomUser(User):
        REQUIRED_FIELDS = ['email']
        USERNAME_FIELD = 'username'
    
    apps.get_app_config('auth').get_model = lambda x: CustomUser if x == 'User' else None
    
    errors = check_user_model(apps.get_app_config('auth').get_models())
    
    assert len(errors) == 0

def test_check_user_model_required_fields_not_list(set_auth_user_model):
    class InvalidUser(User):
        REQUIRED_FIELDS = 'not_a_list'
        USERNAME_FIELD = 'username'

    apps.get_app_config('auth').get_model = lambda x: InvalidUser if x == 'User' else None
    
    errors = check_user_model(apps.get_app_config('auth').get_models())

    assert len(errors) == 1
    assert errors[0].id == 'auth.E001'

def test_check_user_model_username_in_required_fields(set_auth_user_model):
    class InvalidUser(User):
        REQUIRED_FIELDS = ['username']
        USERNAME_FIELD = 'username'

    apps.get_app_config('auth').get_model = lambda x: InvalidUser if x == 'User' else None
    
    errors = check_user_model(apps.get_app_config('auth').get_models())

    assert len(errors) == 1
    assert errors[0].id == 'auth.E002'

def test_check_user_model_username_field_not_unique(set_auth_user_model):
    class InvalidUser(User):
        REQUIRED_FIELDS = []
        USERNAME_FIELD = 'username'

        class Meta:
            unique = False

    apps.get_app_config('auth').get_model = lambda x: InvalidUser if x == 'User' else None
    
    errors = check_user_model(apps.get_app_config('auth').get_models())

    assert len(errors) == 1
    assert errors[0].id == 'auth.E003'

def test_check_user_model_method_instead_of_property(set_auth_user_model):
    class InvalidUser(User):
        REQUIRED_FIELDS = []
        USERNAME_FIELD = 'username'

        def is_anonymous(self):
            return False

        def is_authenticated(self):
            return True

    apps.get_app_config('auth').get_model = lambda x: InvalidUser if x == 'User' else None
    
    errors = check_user_model(apps.get_app_config('auth').get_models())

    assert len(errors) == 2
    assert errors[0].id == 'auth.C009'
    assert errors[1].id == 'auth.C010'