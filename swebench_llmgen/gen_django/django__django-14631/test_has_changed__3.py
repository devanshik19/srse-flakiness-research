import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import BaseForm

class TestBaseForm(BaseForm):
    def __init__(self, data=None, initial=None):
        self.data = data or {}
        self.initial = initial or {}
        self.changed_data = []
        if self.data != self.initial:
            self.changed_data = list(self.data.keys())

def test_has_changed_no_initial_change():
    form = TestBaseForm(data={"username": "user1"}, initial={"username": "user1"})
    assert not form.has_changed()

def test_has_changed_with_initial_change():
    form = TestBaseForm(data={"username": "user2"}, initial={"username": "user1"})
    assert form.has_changed()

def test_has_changed_multiple_fields_change():
    form = TestBaseForm(data={"username": "user3", "email": "user@example.com"}, initial={"username": "user1", "email": "user1@example.com"})
    assert form.has_changed()

def test_has_changed_empty_initial():
    form = TestBaseForm(data={"username": "user4"}, initial={})
    assert form.has_changed()

def test_has_changed_empty_data():
    form = TestBaseForm(data={}, initial={"username": "user5"})
    assert not form.has_changed()