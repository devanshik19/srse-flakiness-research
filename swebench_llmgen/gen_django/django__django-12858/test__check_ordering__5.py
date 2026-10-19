import pytest
from django.core import checks
from django.contrib.auth.models import User

class TestModelChecks:

    @pytest.fixture
    def user_model(self):
        # Dynamically create a model for testing
        class UserModel(User):
            class Meta:
                ordering = ['username']  # Using a field that exists

        return UserModel

    def test_check_ordering_valid(self, user_model):
        assert user_model._check_ordering() == []

    def test_check_ordering_invalid_ordering_type(self, user_model):
        user_model._meta.ordering = 'username'  # Invalid type
        errors = user_model._check_ordering()
        assert len(errors) == 1
        assert errors[0].id == 'models.E014'

    def test_check_ordering_nonexistent_field(self, user_model):
        user_model._meta.ordering = ['nonexistent_field']
        errors = user_model._check_ordering()
        assert len(errors) == 1
        assert errors[0].id == 'models.E015'

    def test_check_ordering_related_field(self, user_model):
        class RelatedModel(User):
            pass
        
        user_model._meta.ordering = ['related_model__nonexistent_field']
        errors = user_model._check_ordering()
        assert len(errors) == 1
        assert errors[0].id == 'models.E015'

    def test_check_ordering_with_pk(self, user_model):
        user_model._meta.ordering = ['pk']  # Valid but should be skipped
        errors = user_model._check_ordering()
        assert errors == []
    
    def test_check_ordering_clash(self, user_model):
        user_model._meta._ordering_clash = True
        errors = user_model._check_ordering()
        assert len(errors) == 1
        assert errors[0].id == 'models.E021'