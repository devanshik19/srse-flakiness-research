import pytest
from django.core import checks
from django.db import models
from django.contrib.auth.models import User

class TestModel(models.Model):
    order_with_respect_to = None
    ordering = []

    class Meta:
        app_label = 'testapp'  # Set a dummy app label

def test_check_ordering_valid_ordering():
    TestModel.ordering = ['username']
    errors = TestModel._check_ordering()
    assert errors == []

def test_check_ordering_invalid_type():
    TestModel.ordering = 'username'
    errors = TestModel._check_ordering()
    assert len(errors) == 1
    assert errors[0].id == 'models.E014'

def test_check_ordering_ordering_with_respect_to():
    TestModel.ordering = ['username']
    TestModel.order_with_respect_to = 'some_field'
    errors = TestModel._check_ordering()
    assert errors == []

def test_check_ordering_nonexistent_field():
    TestModel.ordering = ['nonexistent_field']
    errors = TestModel._check_ordering()
    assert len(errors) == 1
    assert errors[0].id == 'models.E015'

def test_check_ordering_invalid_relational_field():
    TestModel.ordering = ['profile__age']  # Assuming 'profile' does not exist
    errors = TestModel._check_ordering()
    assert len(errors) == 1
    assert errors[0].id == 'models.E015'

def test_check_ordering_valid_multiple_fields():
    TestModel.ordering = ['username', 'email']
    errors = TestModel._check_ordering()
    assert errors == []

def test_check_ordering_excludes_pk_field():
    TestModel.ordering = ['pk']
    errors = TestModel._check_ordering()
    assert errors == []