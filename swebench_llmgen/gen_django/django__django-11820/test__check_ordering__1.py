import pytest
from django.core import checks
from django.db import models
from django.contrib.auth.models import User

class TestModelOrdering:
    class TestModel(models.Model):
        ordering = ['username']  # valid field

    class TestModelWithInvalidField(models.Model):
        ordering = ['invalid_field']  # invalid field

    class TestModelWithRelation(models.Model):
        ordering = ['profile__age']  # assuming a related model profile with an age field

    class TestModelWithOrderingClash(models.Model):
        ordering = ['username']
        order_with_respect_to = 'user'  # clash

    def test_check_ordering_valid(self):
        errors = self.TestModel._check_ordering()
        assert errors == []

    def test_check_ordering_invalid_field(self):
        errors = self.TestModelWithInvalidField._check_ordering()
        assert len(errors) == 1
        assert errors[0].id == 'models.E015'

    def test_check_ordering_related_field(self):
        User.profile = models.OneToOneField('Profile', on_delete=models.CASCADE)
        errors = self.TestModelWithRelation._check_ordering()
        assert errors == []

    def test_check_ordering_with_clash(self):
        errors = self.TestModelWithOrderingClash._check_ordering()
        assert len(errors) == 1
        assert errors[0].id == 'models.E021'

    def test_check_ordering_not_a_list(self):
        class TestModelNotAList(models.Model):
            ordering = 'username'  # incorrect type

        errors = TestModelNotAList._check_ordering()
        assert len(errors) == 1
        assert errors[0].id == 'models.E014'