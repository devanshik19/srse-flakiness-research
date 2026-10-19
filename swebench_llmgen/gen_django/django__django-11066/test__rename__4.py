import pytest
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.db.utils import ProgrammingError

from django.contrib.contenttypes.management import RenameContentType


@pytest.fixture
def rename_content_type():
    return RenameContentType(app_label='auth', old_model='user', new_model='user_renamed')


def test_rename_content_type_success(rename_content_type):
    # Arrange: Create a ContentType for User
    user_content_type = ContentType.objects.get_for_model(User)

    # Act: Rename using _rename
    rename_content_type._rename(global_apps, user_content_type._state.schema, 'user', 'user_renamed')

    # Assert: Check if the model has been renamed
    renamed_content_type = ContentType.objects.get(model='user_renamed')
    assert renamed_content_type.id == user_content_type.id


def test_rename_content_type_does_not_exist(rename_content_type):
    # Act: Try to rename a non-existing content type
    rename_content_type._rename(global_apps, None, 'non_existing_model', 'non_existing_renamed')

    # Assert: No exceptions and ContentType for non_existing_model should not exist
    with pytest.raises(ContentType.DoesNotExist):
        ContentType.objects.get(model='non_existing_model')


def test_rename_content_type_integrity_error(rename_content_type):
    # Arrange: Create a second ContentType for User with the intended new model name to trigger IntegrityError
    ContentType.objects.create(app_label='auth', model='user_renamed')

    # Act: Attempt to rename leading to IntegrityError
    with pytest.raises(IntegrityError):
        rename_content_type._rename(global_apps, None, 'user', 'user_renamed')

    # Assert: Check that the original content type remains unaffected
    user_content_type = ContentType.objects.get(model='user')
    assert user_content_type.model == 'user'


def test_rename_content_type_transactional_rollback(rename_content_type):
    # Arrange: Create another content type and an existing content type with same new model
    ContentType.objects.create(app_label='auth', model='user_renamed')
    initial_count = ContentType.objects.count()

    # Act: Rename which should trigger IntegrityError
    rename_content_type._rename(global_apps, None, 'user', 'user_renamed')

    # Assert: Ensure the number of content types remains unchanged, no permanent changes were made
    assert ContentType.objects.count() == initial_count