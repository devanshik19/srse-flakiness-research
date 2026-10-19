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
    def __init__(self, verbose_name=None, name=None, upload_to=None, storage=None, *args, **kwargs):
        super().__init__(verbose_name, name, *args, **kwargs)
        self.upload_to = upload_to
        self.storage = storage or default_storage

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 100:
            del kwargs["max_length"]
        kwargs['upload_to'] = self.upload_to
        if self.storage is not default_storage:
            kwargs['storage'] = self.storage
        return name, path, args, kwargs

def test_filefield_deconstruct():
    file_field = FileField(verbose_name='Test File', upload_to='uploads/', storage=default_storage)
    name, path, args, kwargs = file_field.deconstruct()
    
    assert name == 'file_field'
    assert path == 'django.db.models.fields.files.FileField'
    assert args == []
    assert kwargs['upload_to'] == 'uploads/'
    assert 'storage' not in kwargs

    file_field_with_max_length = FileField(verbose_name='Test File', upload_to='uploads/', max_length=100)
    name, path, args, kwargs = file_field_with_max_length.deconstruct()
    
    assert 'max_length' not in kwargs