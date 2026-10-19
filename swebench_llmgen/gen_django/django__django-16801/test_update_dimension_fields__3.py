import pytest
from django.contrib.auth.models import User
from django.db import models
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile

class ImageField(models.Field):
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

class ImageModel(models.Model):
    image = ImageField(upload_to='images/', width_field='width', height_field='height')
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

@pytest.mark.django_db
def test_update_dimension_fields():
    user = User.objects.create_user(username='testuser', password='12345')
    file_content = ContentFile(b'fake_image_content')
    image_file = ImageFile(file_content, name='test_image.jpg')
    instance = ImageModel.objects.create(image=image_file)

    # Test if dimensions are set correctly after instance creation
    instance.image.update_dimension_fields(instance)
    assert instance.width is not None
    assert instance.height is not None

    # Clear dimensions and force update
    instance.width = None
    instance.height = None
    instance.image.update_dimension_fields(instance, force=True)
    assert instance.width is not None
    assert instance.height is not None

    # Ensure dimensions are not updated if they are already filled and force is False
    original_width = instance.width
    original_height = instance.height
    instance.image.update_dimension_fields(instance)
    assert instance.width == original_width
    assert instance.height == original_height

    # Test when no file is assigned
    instance.image = None
    instance.image.update_dimension_fields(instance)
    assert instance.width is None
    assert instance.height is None