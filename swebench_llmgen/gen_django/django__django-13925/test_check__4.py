import pytest
from django.contrib.auth.models import User

def test_check_without_swappable():
    user = User(username='testuser')
    user.save()
    
    # No custom swapping, using the default User model
    errors = User.check()

    # Assert that no errors are returned for a valid model
    assert len(errors) == 0

def test_check_with_swappable():
    class CustomUser(User):
        class Meta:
            swappable = 'AUTH_USER_MODEL'

    errors = CustomUser.check()

    # Check that swappable model has no errors to report
    assert len(errors) == 0

def test_check_with_field_clashes():
    class ClashingUser(User):
        username = None  # This will cause a field clash

    errors = ClashingUser.check()

    # Assert that errors are returned due to field clashes
    assert any("Field 'username'" in str(error) for error in errors)

def test_check_with_long_column_names():
    class LongNameUser(User):
        very_long_column_name_that_exceeds_the_limit = None

    errors = LongNameUser.check()

    # Assert errors related to long column names 
    assert any("Long column names" in str(error) for error in errors)

def test_check_with_unique_constraints():
    class UniqueUser(User):
        class Meta:
            unique_together = (('username',),)

    errors = UniqueUser.check()

    # No errors should occur on valid unique constraints
    assert len(errors) == 0