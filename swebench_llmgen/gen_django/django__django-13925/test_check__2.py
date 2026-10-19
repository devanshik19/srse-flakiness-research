import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

@pytest.mark.parametrize("databases, expected_error_count", [
    (None, 0),  # No databases provided, expect no errors
    ([], 0),    # Empty list, expect no errors
])
def test_check_no_errors(databases, expected_error_count):
    # Arrange
    user_model = User
    
    # Act
    errors = user_model.check(databases=databases)
    
    # Assert
    assert len(errors) == expected_error_count

def test_check_with_field_name_clashes():
    # Arrange: Create a model with a potential field name clash
    class ClashingModel(User):
        username = None  # This will clash with Django's default username field
        
    # Act & Assert
    errors = ClashingModel.check()
    assert any('username' in str(error) for error in errors)  # Check for specific error

def test_check_non_swapped_model():
    # Arrange: Create a non-swappable model
    class NonSwappableModel(User):
        class Meta:
            swappable = False
    
    # Act
    errors = NonSwappableModel.check()
    
    # Assert: Should not have any errors
    assert len(errors) == 0

def test_check_unique_constraint_errors():
    # Arrange: Create a model with unique constraint
    class UniqueConstraintModel(User):
        class Meta:
            unique_together = (("username",),)
    
    # Create a User instance with the same username
    User.objects.create_user(username='testuser', password='pass')
    
    # Act & Assert: Attempt to create a duplicate should give a ValidationError
    with pytest.raises(ValidationError):
        User.objects.create_user(username='testuser', password='pass')

def test_check_with_long_column_names():
    # Arrange: Create a model with a long column name
    class LongColumnModel(User):
        long_field_name_that_exceeds_the_limit = None
        
        class Meta:
            db_table = 'long_table_name'

    # Act
    errors = LongColumnModel.check()
    
    # Assert: Look for specific long column name error
    assert any('long_field_name_that_exceeds_the_limit' in str(error) for error in errors)