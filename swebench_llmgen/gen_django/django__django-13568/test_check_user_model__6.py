import pytest
from django.contrib.auth.models import User
from django.apps import apps
from django.conf import settings
from django.core import checks
from itertools import chain

def test_check_user_model_no_app_configs():
    # Arrange
    errors = check_user_model()

    # Assert that no errors are raised when using the default User model
    assert len(errors) == 0

def test_check_user_model_required_fields_not_list():
    # Arrange
    class InvalidUserModel(User):
        REQUIRED_FIELDS = 'not_a_list'

    apps.get_model = lambda app_label, model_name: InvalidUserModel

    # Act
    errors = check_user_model(apps.get_app_configs())

    # Assert
    assert len(errors) == 1
    assert errors[0].id == 'auth.E001'

def test_check_user_model_username_field_in_required_fields():
    # Arrange
    class InvalidUserModel(User):
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = ['username']

    apps.get_model = lambda app_label, model_name: InvalidUserModel

    # Act
    errors = check_user_model(apps.get_app_configs())

    # Assert
    assert len(errors) == 1
    assert errors[0].id == 'auth.E002'

def test_check_user_model_username_field_not_unique():
    # Arrange
    class NonUniqueUserModel(User):
        USERNAME_FIELD = 'username'

        class Meta:
            constraints = []

    apps.get_model = lambda app_label, model_name: NonUniqueUserModel
    settings.AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

    # Act
    errors = check_user_model(apps.get_app_configs())

    # Assert
    assert len(errors) == 1
    assert errors[0].id == 'auth.E003'

def test_check_user_model_username_field_not_unique_warning():
    # Arrange
    class NonUniqueUserModel(User):
        USERNAME_FIELD = 'username'

        class Meta:
            constraints = []

    apps.get_model = lambda app_label, model_name: NonUniqueUserModel
    settings.AUTHENTICATION_BACKENDS = ['custom.backend']

    # Act
    errors = check_user_model(apps.get_app_configs())

    # Assert
    assert len(errors) == 1
    assert errors[0].id == 'auth.W004'

def test_check_user_model_is_anonymous_method():
    # Arrange
    class InvalidUserModel(User):
        USERNAME_FIELD = 'username'

        def is_anonymous(self):
            return False

    apps.get_model = lambda app_label, model_name: InvalidUserModel

    # Act
    errors = check_user_model(apps.get_app_configs())

    # Assert
    assert len(errors) == 1
    assert errors[0].id == 'auth.C009'

def test_check_user_model_is_authenticated_method():
    # Arrange
    class InvalidUserModel(User):
        USERNAME_FIELD = 'username'

        def is_authenticated(self):
            return True

    apps.get_model = lambda app_label, model_name: InvalidUserModel

    # Act
    errors = check_user_model(apps.get_app_configs())

    # Assert
    assert len(errors) == 1
    assert errors[0].id == 'auth.C010'