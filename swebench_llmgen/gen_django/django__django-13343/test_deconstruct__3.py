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

class FileField(Field):
    def __init__(self, verbose_name=None, name=None, upload_to=None, storage=default_storage, **kwargs):
        super().__init__(verbose_name, name, **kwargs)
        self.upload_to = upload_to
        self.storage = storage

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 100:
            del kwargs["max_length"]
        kwargs['upload_to'] = self.upload_to
        if self.storage is not default_storage:
            kwargs['storage'] = self.storage
        return name, path, args, kwargs

def test_file_field_deconstruct():
    field = FileField(max_length=100, upload_to='uploads/', storage=Storage())
    
    name, path, args, kwargs = field.deconstruct()

    assert name == 'file'  # Assuming 'file' used in Field superclass
    assert path == 'django.db.models.fields.files.FileField'
    assert args == []
    assert 'upload_to' in kwargs
    assert kwargs['upload_to'] == 'uploads/'
    assert 'storage' in kwargs
    assert kwargs['storage'] == field.storage
    
    # Now testing the case when max_length is 100
    field_with_max_length = FileField(max_length=100, upload_to='uploads/')
    name, path, args, kwargs = field_with_max_length.deconstruct()
    
    assert 'max_length' not in kwargs