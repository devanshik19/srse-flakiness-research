import datetime
import posixpath
from django import forms
from django.core import checks
from django.core.files.base import File
from django.core.files.images import ImageFile
from django.core.files.storage import Storage, default_storage
from django.core.files.utils import validate_file_name
from django.db.models import signals
from django.db.models.fields import Field
from django.db.models.query_utils import DeferredAttribute
from django.db.models.utils import AltersData
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class FileField(Field):
    def __init__(self, verbose_name=None, name=None, upload_to=None, storage=None, **kwargs):
        super().__init__(verbose_name, name, **kwargs)
        self.upload_to = upload_to
        self.storage = storage or default_storage

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 100:
            del kwargs["max_length"]
        kwargs["upload_to"] = self.upload_to
        if self.storage is not default_storage:
            kwargs["storage"] = getattr(self, "_storage_callable", self.storage)
        return name, path, args, kwargs

def test_deconstruct():
    field = FileField(upload_to='uploads/', storage=Storage())

    # Test with default max_length
    name, path, args, kwargs = field.deconstruct()
    assert kwargs['upload_to'] == 'uploads/'
    assert 'storage' not in kwargs

    # Test with max_length set to 100
    field.max_length = 100
    name, path, args, kwargs = field.deconstruct()
    assert 'max_length' not in kwargs

    # Test with a different storage
    field.storage = Storage()
    name, path, args, kwargs = field.deconstruct()
    assert kwargs['storage'] == field.storage