import pytest
from django.core import checks
from django.db import models
from django.contrib.auth.models import User

class TestModelOrderingChecks:

    class TestModel(models.Model):
        ordering = []
        order_with_respect_to = None
        class Meta:
            app_label = 'testapp'

    def test_check_ordering_clash(self):
        self.TestModel.ordering = ['field1']
        self.TestModel._meta._ordering_clash = True
        errors = self.TestModel._check_ordering()
        assert len(errors) == 1
        assert errors[0].id == 'models.E021'

    def test_ordering_not_a_list_or_tuple(self):
        self.TestModel.ordering = 'field1'
        errors = self.TestModel._check_ordering()
        assert len(errors) == 1
        assert errors[0].id == 'models.E014'

    def test_missing_fields_in_ordering(self):
        self.TestModel.ordering = ['nonexistent_field']
        # Create a model instance to set _meta from User
        user = User(username='testuser')
        user.save()
        self.TestModel._meta = user._meta  # Mock setting to reference User fields
        errors = self.TestModel._check_ordering()
        assert len(errors) == 1
        assert errors[0].id == 'models.E015'

    def test_check_valid_ordering(self):
        self.TestModel.ordering = ['username']
        user = User(username='testuser')
        user.save()
        self.TestModel._meta = user._meta  # Mock setting to reference User fields
        errors = self.TestModel._check_ordering()
        assert len(errors) == 0

    def test_check_invalid_related_field(self):
        self.TestModel.ordering = ['profile__bio']
        # Hooking into the User model which does not have a 'profile' related field
        user = User(username='testuser')
        user.save()
        self.TestModel._meta = user._meta  # Mock setting to reference User fields
        errors = self.TestModel._check_ordering()
        assert len(errors) == 1
        assert errors[0].id == 'models.E015'

    def test_skip_primary_key_field(self):
        self.TestModel.ordering = ['pk']
        user = User(username='testuser')
        user.save()
        self.TestModel._meta = user._meta  # Mock setting to reference User fields
        errors = self.TestModel._check_ordering()
        assert len(errors) == 0