import pytest
from django.contrib.auth.models import User
from django.db.models.fields import AutoFieldMeta

class TestAutoFieldMeta:
    @pytest.fixture
    def auto_field_meta(self):
        class CustomAutoFieldMeta(AutoFieldMeta):
            _subclasses = (User,)

        return CustomAutoFieldMeta()

    def test_instancecheck_with_subclass(self, auto_field_meta):
        user_instance = User(username='testuser')
        assert auto_field_meta.__instancecheck__(user_instance) is True

    def test_instancecheck_without_subclass(self, auto_field_meta):
        class NonUser:
            pass
        
        non_user_instance = NonUser()
        assert auto_field_meta.__instancecheck__(non_user_instance) is False

    def test_instancecheck_with_superclass(self, auto_field_meta):
        assert auto_field_meta.__instancecheck__(auto_field_meta) is False  # Meta class itself isn't an instance of _subclasses