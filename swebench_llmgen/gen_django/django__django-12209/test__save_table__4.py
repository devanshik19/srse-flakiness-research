import pytest
from django.contrib.auth.models import User
from django.db import DatabaseError

@pytest.mark.parametrize(
    "update_fields, force_insert, force_update, expected_exception",
    [
        (None, False, False, None),                             # Basic save
        (['username'], False, False, None),                    # Update specified field
        (['username'], False, True, DatabaseError),            # Force update without pk
        (None, True, False, None),                             # Insert new instance
    ]
)
def test_save_table(update_fields, force_insert, force_update, expected_exception):
    user = User(username='testuser')
    
    if expected_exception:
        with pytest.raises(expected_exception):
            user._save_table(cls=User, force_insert=force_insert, 
                             force_update=force_update, 
                             update_fields=update_fields)
    else:
        user._save_table(cls=User, force_insert=force_insert, 
                         force_update=force_update, 
                         update_fields=update_fields)
        # Verify that the user instance has been saved correctly
        saved_user = User.objects.get(username='testuser')
        assert saved_user.username == 'testuser'