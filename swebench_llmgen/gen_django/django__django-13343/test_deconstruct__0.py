import datetime
import posixpath
from django import forms
from django.core import checks
from django.core.files.base import File
from django.core.files.images import ImageFile
from django.core.files.storage import Storage, default_storage
from django.db import models
from django.db.models import signals
from django.db.models.fields import Field
from django.db.models.query_utils import DeferredAttribute
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
import pytest

class FileField(Field):
    def __init__(self, verbose_name=None, name=None, upload_to=None, storage=None, **kwargs):
        self.upload_to = upload_to
        self.storage = storage or default_storage
        super().__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 100:
            del kwargs["max_length"]
        kwargs['upload_to'] = self.upload_to
        if self.storage is not default_storage:
            kwargs['storage'] = self.storage
        return name, path, args, kwargs

@pytest.mark.parametrize('max_length, expected_kwargs', [
    (100, {'upload_to': None}),  # Case when max_length=100, 'max_length' should be deleted
    (None, {'upload_to': None, 'storage': default_storage}),  # Normal case
])
def test_deconstruct(max_length, expected_kwargs):
    field = FileField(upload_to=None, storage=default_storage, max_length=max_length)
    name, path, args, kwargs = field.deconstruct()

    assert 'max_length' not in kwargs
    assert kwargs['upload_to'] == expected_kwargs['upload_to']
    assert kwargs.get('storage', default_storage) == expected_kwargs.get('storage', default_storage)

    # Check that name and path are consistent with the base class Field
    assert name == field.name
    assert path == 'django.db.models.fields.files.FileField'  # Expected path for FileField