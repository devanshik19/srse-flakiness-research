import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError

@pytest.mark.django_db
def test_prepare_related_fields_for_save_with_unsaved_related_object():
    user1 = User(username='user1')
    user1.save()

    user2 = User(username='user2')
    user2.save()
    
    # Creating a related object without saving it
    user3 = User(username='user3')
    
    # Trying to assign an unsaved related object should raise ValueError
    user1.profile = user3  # Assuming Profile has a OneToOneField to User
    with pytest.raises(ValueError, match="prohibited to prevent data loss due to unsaved related object 'profile'."):
        user1._prepare_related_fields_for_save('save')

def test_prepare_related_fields_for_save_with_saved_related_object():
    user1 = User(username='user1')
    user1.save()

    user2 = User(username='user2')
    user2.save()
    
    # Properly assigning a saved related object
    user1.profile = user2  # Assuming Profile has a OneToOneField to User
    user1.profile.save()
    
    # Should not raise an error
    try:
        user1._prepare_related_fields_for_save('save')
    except Exception:
        pytest.fail("Unexpected exception raised during valid related field save.")
    
    # Make sure the attribute is set correctly
    assert user1.profile.pk == user2.pk