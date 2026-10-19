import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import ForeignKey
from django.db import models

class TestForeignKeyValidation:
    
    class MockModel(models.Model):
        user = ForeignKey(User, on_delete=models.CASCADE)

    @pytest.fixture
    def user_instance(self):
        return User.objects.create(username='testuser')

    @pytest.fixture
    def mock_instance(self, user_instance):
        return self.MockModel.objects.create(user=user_instance)

    def test_validate_with_valid_user(self, user_instance, mock_instance):
        # Should not raise ValidationError
        try:
            mock_instance.user.field.remote_field.validate(user_instance.pk, mock_instance)
        except ValidationError:
            pytest.fail("ValidationError was raised unexpectedly!")

    def test_validate_with_invalid_user(self, mock_instance):
        invalid_user_id = 999  # Assuming this ID does not exist
        with pytest.raises(ValidationError) as excinfo:
            mock_instance.user.field.remote_field.validate(invalid_user_id, mock_instance)
        
        assert excinfo.value.code == 'invalid'
        assert 'testuser' not in str(excinfo.value)  # Verify specific error message

    def test_validate_with_none_value(self, mock_instance):
        # Should not raise ValidationError when value is None
        try:
            mock_instance.user.field.remote_field.validate(None, mock_instance)
        except ValidationError:
            pytest.fail("ValidationError was raised unexpectedly for None value!")

    def test_validate_with_parent_link(self):
        # Test to skip validation when parent_link is True
        fkey = ForeignKey(User, on_delete=models.CASCADE, parent_link=True)
        try:
            fkey.validate(1, None)  # Should not raise
        except ValidationError:
            pytest.fail("ValidationError was raised unexpectedly for parent_link!")