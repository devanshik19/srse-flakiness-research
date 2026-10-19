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
from django.db import models

class SampleFileField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = default_storage

class TestFieldFile:
    def test_init(self):
        user = User.objects.create(username='testuser', password='password')
        file_field = SampleFileField()
        field_file = FieldFile(instance=user, field=file_field, name='profile_picture')
        
        assert field_file.instance == user
        assert field_file.field == file_field
        assert field_file.storage == file_field.storage
        assert field_file._committed is True