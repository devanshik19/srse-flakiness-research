import datetime
import posixpath
from django import forms
from django.core import checks
from django.core.files.base import File
from django.core.files.images import ImageFile
from django.core.files.storage import Storage, default_storage
from django.db.models import signals
from django.db.models.fields import Field
from django.db.models.query_utils import DeferredAttribute
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class FileField(Field):
    def __init__(self, verbose_name=None, name=None, upload_to=None, storage=default_storage, **kwargs):
        self.upload_to = upload_to
        self.storage = storage
        super().__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 100:
            del kwargs["max_length"]
        kwargs['upload_to'] = self.upload_to
        if self.storage is not default_storage:
            kwargs['storage'] = self.storage
        return name, path, args, kwargs

def test_file_field_deconstruct():
    field = FileField(upload_to='uploads/', storage=default_storage)

    name, path, args, kwargs = field.deconstruct()
    
    assert name == 'filefield'
    assert path == 'django.db.models.fields.files.FileField'
    assert args == []
    assert kwargs['upload_to'] == 'uploads/'
    assert 'storage' not in kwargs  # Check default_storage is not included

    # Test with max_length set to 100
    field_with_max_length = FileField(upload_to='uploads/', storage=default_storage, max_length=100)
    name, path, args, kwargs = field_with_max_length.deconstruct()

    assert 'max_length' not in kwargs  # Check max_length is removed