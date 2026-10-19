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
from django.db import models

class ImageField(Field):
    attr_class = ImageFile
    descriptor_class = None
    description = _('Image field')

    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        self.width_field = width_field
        self.height_field = height_field
        super().__init__(verbose_name, name, **kwargs)

    def update_dimension_fields(self, instance, force=False, *args, **kwargs):
        has_dimension_fields = self.width_field or self.height_field
        if not has_dimension_fields or self.attname not in instance.__dict__:
            return

        file = getattr(instance, self.attname)

        if not file and not force:
            return

        dimension_fields_filled = not (
            (self.width_field and not getattr(instance, self.width_field))
            or (self.height_field and not getattr(instance, self.height_field))
        )
        if dimension_fields_filled and not force:
            return

        if file:
            width = file.width
            height = file.height
        else:
            width = None
            height = None

        if self.width_field:
            setattr(instance, self.width_field, width)
        if self.height_field:
            setattr(instance, self.height_field, height)

def test_update_dimension_fields():
    class TestModel(models.Model):
        image = ImageField(width_field='width', height_field='height')
        width = models.PositiveIntegerField(null=True)
        height = models.PositiveIntegerField(null=True)

    user = User(username='testuser')
    user.save()

    instance = TestModel(image=ImageFile(open('test_image.jpg', 'rb')), width=None, height=None)
    instance.save()

    field = instance._meta.get_field('image')
    field.attname = 'image'
    
    # Test dimensions update when image is present
    field.update_dimension_fields(instance)
    assert instance.width is not None
    assert instance.height is not None
    
    # Test that dimensions are not updated if they are already filled
    field.update_dimension_fields(instance)
    assert instance.width is not None
    assert instance.height is not None

    # Test with force parameter
    field.update_dimension_fields(instance, force=True)
    assert instance.width is not None
    assert instance.height is not None

    # Test with no image, should clear dimensions
    instance.image = None
    field.update_dimension_fields(instance)
    assert instance.width is None
    assert instance.height is None