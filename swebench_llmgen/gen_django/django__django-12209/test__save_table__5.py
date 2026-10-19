import pytest
from django.contrib.auth.models import User
from django.db import DEFAULT_DB_ALIAS, DatabaseError

@pytest.mark.parametrize("force_insert, force_update, update_fields, expected_exception", [
    (False, False, None, None),             # Normal case, expect no exception
    (False, True, None, ValueError),        # Force update without primary key
    (True, False, None, None),              # Force insert when adding instance
    (False, False, ['username'], DatabaseError),  # Update field not affected
])
def test_save_table(force_insert, force_update, update_fields, expected_exception):
    user = User(username='testuser', password='testpassword')
    
    try:
        user._save_table(raw=False, cls=User, force_insert=force_insert, 
                         force_update=force_update, using=DEFAULT_DB_ALIAS, 
                         update_fields=update_fields)
        if expected_exception:
            pytest.fail(f"Expected exception {expected_exception} but none was raised.")
    except Exception as e:
        if expected_exception:
            assert isinstance(e, expected_exception)
        else:
            pytest.fail(f"Unexpected exception raised: {type(e).__name__}")

    # Ensure the user is saved correctly
    if not expected_exception:
        user.save()
        assert User.objects.filter(username='testuser').exists()