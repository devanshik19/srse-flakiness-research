import pytest
from django.contrib.auth.models import User
from django.db.models.fields.related_descriptors import ForeignKeyDeferredAttribute


class TestForeignKeyDeferredAttribute:
    @pytest.fixture
    def setup_instance(self):
        user = User(username='testuser', password='testpass')
        user.save()
        return user

    def test_set_new_value_creates_entry(self, setup_instance):
        # Assuming a ForeignKeyDeferredAttribute instance
        def mock_field_deletion(instance):
            instance.__dict__.pop('related_user_id', None)

        field = ForeignKeyDeferredAttribute()
        field.field = type('MockField', (), {
            'attname': 'related_user_id',
            'is_cached': lambda inst: 'related_user_id' in inst.__dict__,
            'delete_cached_value': mock_field_deletion
        })()

        # First set
        field.__set__(setup_instance, 1)
        assert setup_instance.__dict__['related_user_id'] == 1

    def test_set_same_value_does_not_delete_cache(self, setup_instance):
        def mock_field_deletion(instance):
            instance.__dict__.pop('related_user_id', None)

        field = ForeignKeyDeferredAttribute()
        field.field = type('MockField', (), {
            'attname': 'related_user_id',
            'is_cached': lambda inst: 'related_user_id' in inst.__dict__,
            'delete_cached_value': mock_field_deletion
        })()

        # Initial set
        field.__set__(setup_instance, 1)
        assert setup_instance.__dict__['related_user_id'] == 1

        # Set the same value
        field.__set__(setup_instance, 1)
        assert setup_instance.__dict__['related_user_id'] == 1

    def test_set_different_value_deletes_cache(self, setup_instance):
        def mock_field_deletion(instance):
            instance.__dict__.pop('related_user_id', None)

        field = ForeignKeyDeferredAttribute()
        field.field = type('MockField', (), {
            'attname': 'related_user_id',
            'is_cached': lambda inst: 'related_user_id' in inst.__dict__,
            'delete_cached_value': mock_field_deletion
        })()

        # Initial set
        field.__set__(setup_instance, 1)
        assert setup_instance.__dict__['related_user_id'] == 1

        # Set a different value
        field.__set__(setup_instance, 2)
        assert setup_instance.__dict__['related_user_id'] == 2

        # Check if the cache got deleted
        assert 'related_user_id' not in setup_instance.__dict__