import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def test_model_check_on_user():
    user = User(username='testuser', email='test@example.com')
    
    # Check validation errors when saving an incomplete user object
    with pytest.raises(ValidationError):
        user.full_clean()  # Does not have a password set

    # We shouldn't get any errors during the model's check method
    errors = User.check()
    assert len(errors) == 0

    # Setting a password should allow the user model to be valid
    user.set_password('testpassword')
    
    # Now it should not raise any validation errors
    try:
        user.full_clean()  # Validating with password set
    except ValidationError as e:
        pytest.fail(f"Unexpected ValidationError raised: {e}")

    # Check again that there are still no model errors
    errors_after_set_password = User.check()
    assert len(errors_after_set_password) == 0