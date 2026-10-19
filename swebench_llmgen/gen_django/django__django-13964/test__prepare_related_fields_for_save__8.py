import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValueError

@pytest.mark.parametrize("operation_name", ["create", "update"])
@pytest.mark.parametrize("related_obj_pk", [None, 1])
def test_prepare_related_fields_for_save(operation_name, related_obj_pk):
    # Set up a user instance
    user = User(username='testuser')
    
    # If related_obj_pk is None, we simulate an unsaved related object
    related_user = User(username='relateduser') if related_obj_pk is not None else None
    
    # Assign the related user to the user instance
    if related_user is not None:
        related_user.save()  # Save related_user to assign a PK
    
    # Simulate a ForeignKey by creating the relationship manually
    if related_obj_pk is None:
        # Simulate unsaved related object
        user.profile = related_user  # Assuming a one-to-one profile relationship
    else:
        user.profile_id = related_obj_pk  # Assuming related user's pk is set
    
    if related_obj_pk is None:
        with pytest.raises(ValueError, match="prohibited to prevent data loss due to unsaved related object"):
            user._prepare_related_fields_for_save(operation_name)
    else:
        user._prepare_related_fields_for_save(operation_name)
        assert user.profile_id == related_user.id