import pytest
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.db.utils import OperationalError

from django.contrib.contenttypes.management import RenameContentType

@pytest.mark.django_db
def test_rename_content_type():
    # Setup
    app_label = 'auth'
    old_model = 'user'
    new_model = 'renamed_user'
    
    # Create initial ContentType
    user_content_type = ContentType.objects.create(app_label=app_label, model=old_model)

    # Create RenameContentType instance
    renamer = RenameContentType(app_label, old_model, new_model)

    # Test renaming existing ContentType
    renamer._rename(apps, apps.schema_editor(), old_model, new_model)
    updated_content_type = ContentType.objects.get(id=user_content_type.id)
    assert updated_content_type.model == new_model
    
    # Test renaming should not affect the caching
    ContentType.objects.clear_cache()
    assert ContentType.objects.get_by_natural_key(app_label, new_model) == updated_content_type

    # Test renaming raises IntegrityError when trying to rename to an existing model
    duplicate_content_type = ContentType.objects.create(app_label=app_label, model=new_model)

    with pytest.raises(IntegrityError):
        renamer._rename(apps, apps.schema_editor(), new_model, 'another_renamed_user')

    # Test fallback to old model name when an error occurs
    renamer._rename(apps, apps.schema_editor(), old_model, 'another_renamed_user')
    assert ContentType.objects.get(id=user_content_type.id).model == new_model

    # Cleanup
    duplicate_content_type.delete()