import pytest
from django.contrib.auth.models import User
from django.db import models
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage

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

class MyModel(models.Model):
    image = ImageField(upload_to='images', width_field='image_width', height_field='image_height')
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)

@pytest.mark.parametrize("force,expected_width,expected_height", [
    (False, None, None),  # No image provided
    (True, 100, 200),     # Image dimensions to be forced set
])
def test_update_dimension_fields(force, expected_width, expected_height):
    # Create a temporary image
    image_file = ContentFile(b"dummy image content")
    file_name = 'test_image.png'
    filepath = default_storage.save(file_name, image_file)
    image = ImageFile(default_storage.open(filepath))

    user = User.objects.create(username='testuser')
    instance = MyModel.objects.create(image=image)

    # Invoke the update_dimension_fields method
    instance.image.update_dimension_fields(instance, force)

    # Assert the width and height fields
    assert instance.image_width == expected_width
    assert instance.image_height == expected_height

    # Clean up
    default_storage.delete(filepath)