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

class TestFileField:
    def setup_method(self):
        self.upload_to = 'uploads/'
        self.storage = default_storage
        self.file_field = FileField(verbose_name='File', name='file', upload_to=self.upload_to, storage=self.storage)

    def test_deconstruct_without_max_length(self):
        self.file_field.max_length = None  # Simulating no max_length
        name, path, args, kwargs = self.file_field.deconstruct()
        assert kwargs.get("max_length") is None
        assert kwargs['upload_to'] == self.upload_to
        assert kwargs['storage'] == self.storage

    def test_deconstruct_with_max_length(self):
        self.file_field.max_length = 100  # Simulating max_length
        name, path, args, kwargs = self.file_field.deconstruct()
        assert "max_length" not in kwargs  # It should be deleted
        assert kwargs['upload_to'] == self.upload_to
        assert kwargs['storage'] == self.storage

    def test_deconstruct_with_custom_storage(self):
        custom_storage = Storage()  # Simulating custom storage (should work without errors)
        self.file_field.storage = custom_storage
        name, path, args, kwargs = self.file_field.deconstruct()
        assert kwargs['storage'] == custom_storage  # Custom storage should be retained