import pytest
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db import transaction

from django.contrib.contenttypes.management import RenameContentType

@pytest.mark.django_db
def test_rename_content_type():
    app_label = 'auth'
    old_model = 'user'
    new_model = 'new_user'

    # Create an initial content type for the User model
    content_type = ContentType.objects.create(app_label=app_label, model=old_model)

    # Instantiate the RenameContentType class
    renamer = RenameContentType(app_label, old_model, new_model)

    # Get the schema editor
    schema_editor = transaction.get_connection().schema_editor()

    # Perform the rename operation
    renamer._rename(global_apps, schema_editor, old_model, new_model)

    # Fetch the content type again after renaming
    updated_content_type = ContentType.objects.get(pk=content_type.pk)

    # Check that the model name has been updated
    assert updated_content_type.model == new_model

    # Check that the cache has been cleared by trying to get old content type
    with pytest.raises(ContentType.DoesNotExist):
        ContentType.objects.get_by_natural_key(app_label, old_model)

    # Now test a rename that causes an IntegrityError
    another_content_type = ContentType.objects.create(app_label=app_label, model=new_model)

    # Try to rename again with the same new model name
    renamer._rename(global_apps, schema_editor, old_model, new_model)

    # Fetch the content type again
    final_content_type = ContentType.objects.get(pk=updated_content_type.pk)

    # The content type should revert back to old_model due to IntegrityError
    assert final_content_type.model == old_model