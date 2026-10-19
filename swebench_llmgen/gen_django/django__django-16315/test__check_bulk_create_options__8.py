import pytest
from django.db import connections, NotSupportedError
from django.db.models import QuerySet
from django.contrib.auth.models import User


class TestQuerySet:
    @pytest.fixture
    def queryset(self):
        return QuerySet(model=User)

    def test_check_bulk_create_options_ignore_conflicts(self, queryset):
        assert queryset._check_bulk_create_options(True, False, None, None) == OnConflict.IGNORE

    def test_check_bulk_create_options_update_conflicts(self, queryset):
        assert queryset._check_bulk_create_options(False, True, ['username'], ['email']) == OnConflict.UPDATE

    def test_check_bulk_create_options_mutually_exclusive(self, queryset):
        with pytest.raises(ValueError, match="mutually exclusive"):
            queryset._check_bulk_create_options(True, True, None, None)

    def test_check_bulk_create_options_without_update_fields(self, queryset):
        with pytest.raises(ValueError, match="must be provided"):
            queryset._check_bulk_create_options(False, True, [], ['email'])

    def test_check_bulk_create_options_without_unique_fields(self, queryset):
        with pytest.raises(ValueError, match="must be provided"):
            queryset._check_bulk_create_options(False, True, ['username'], [])

    def test_check_bulk_create_options_update_fields_primary_key(self, queryset):
        User._meta.get_field('username').primary_key = True
        with pytest.raises(ValueError, match="cannot be used with primary keys"):
            queryset._check_bulk_create_options(False, True, ['username'], ['email'])

    def test_check_bulk_create_options_update_fields_concrete(self, queryset):
        User._meta.get_field('username').concrete = False
        with pytest.raises(ValueError, match="can only be used with concrete fields"):
            queryset._check_bulk_create_options(False, True, ['username'], ['email'])

    def test_check_bulk_create_options_not_supported(self, queryset):
        conn = connections[queryset.db]
        conn.features.supports_ignore_conflicts = False
        with pytest.raises(NotSupportedError, match="does not support ignoring conflicts"):
            queryset._check_bulk_create_options(True, False, None, None)

        conn.features.supports_update_conflicts = False
        with pytest.raises(NotSupportedError, match="does not support updating conflicts"):
            queryset._check_bulk_create_options(False, True, ['username'], ['email'])