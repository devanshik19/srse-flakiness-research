import pytest
from django.core import checks
from django.db import models
from django.contrib.auth.models import User

class TestModelOrdering:

    class TestModel(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        _meta = models.Options()

    def test_ordering_valid(self):
        self.TestModel._meta.ordering = ['user']
        errors = self.TestModel._check_ordering()
        assert errors == []

    def test_ordering_invalid_non_field(self):
        self.TestModel._meta.ordering = ['non_existent_field']
        errors = self.TestModel._check_ordering()
        assert len(errors) == 1
        assert errors[0].id == 'models.E015'

    def test_ordering_invalid_type(self):
        self.TestModel._meta.ordering = 'invalid_type'
        errors = self.TestModel._check_ordering()
        assert len(errors) == 1
        assert errors[0].id == 'models.E014'

    def test_ordering_with_clash(self):
        self.TestModel._meta._ordering_clash = True
        self.TestModel._meta.ordering = ['user']
        errors = self.TestModel._check_ordering()
        assert len(errors) == 1
        assert errors[0].id == 'models.E021'

    def test_ordering_with_related_field(self):
        self.TestModel._meta.ordering = ['user__username']
        errors = self.TestModel._check_ordering()
        assert errors == []