import pytest
from django.contrib.auth.models import User
from django.db import NotSupportedError
from django.db.models import QuerySet

class TestQuerySet:

    def setup_method(self):
        self.queryset = QuerySet(User)

    def test_check_bulk_create_options_ignore_conflicts(self):
        assert self.queryset._check_bulk_create_options(True, False, None, None) == OnConflict.IGNORE

    def test_check_bulk_create_options_update_conflicts(self):
        with pytest.raises(ValueError, match="ignore_conflicts and update_conflicts are mutually exclusive."):
            self.queryset._check_bulk_create_options(True, True, None, None)

        with pytest.raises(NotSupportedError, match="This database backend does not support ignoring conflicts."):
            self.queryset._check_bulk_create_options(True, False, None, None)
        
        # Simulate a database feature check for supported conflicts
        db_features = self.queryset.db.features
        original_support_update = db_features.supports_update_conflicts
        db_features.supports_update_conflicts = False

        with pytest.raises(NotSupportedError, match="This database backend does not support updating conflicts."):
            self.queryset._check_bulk_create_options(False, True, None, None)

        db_features.supports_update_conflicts = True
        with pytest.raises(ValueError, match="Fields that will be updated when a row insertion fails on conflicts must be provided."):
            self.queryset._check_bulk_create_options(False, True, None, None)

        with pytest.raises(ValueError, match="Unique fields that can trigger the upsert must be provided."):
            self.queryset._check_bulk_create_options(False, True, ['field1'], None)

        # Restore original features
        db_features.supports_update_conflicts = original_support_update

    def test_check_bulk_create_options_invalid_update_fields(self):
        with pytest.raises(ValueError, match="bulk_create() can only be used with concrete fields in update_fields."):
            self.queryset._check_bulk_create_options(False, True, ['nonexistent_field'], None)

    def test_check_bulk_create_options_invalid_unique_fields(self):
        with pytest.raises(ValueError, match="bulk_create() can only be used with concrete fields in unique_fields."):
            self.queryset._check_bulk_create_options(False, True, ['field1'], ['nonexistent_field'])