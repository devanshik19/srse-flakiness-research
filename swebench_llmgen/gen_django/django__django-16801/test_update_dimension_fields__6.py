import pytest
from django.contrib.auth.models import User
from django.db import models
from django.core.files.base import File
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage

class ImageField(models.Field):
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        super().__init__(verbose_name, name, **kwargs)
        self.width_field = width_field
        self.height_field = height_field
        self.attname = 'image'

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
    image = ImageField(width_field='image_width', height_field='image_height')
    image_width = models.PositiveIntegerField(null=True, blank=True)
    image_height = models.PositiveIntegerField(null=True, blank=True)

@pytest.mark.django_db
def test_update_dimension_fields():
    user = User.objects.create_user(username='testuser', password='12345')
    image_file = ImageFile(File(open('path/to/test/image.jpg', 'rb')))
    user.image.save('test_image.jpg', image_file)

    # Initially, width and height should be None
    assert user.image_width is None
    assert user.image_height is None

    # Call the update_dimension_fields method without force
    user.image.update_dimension_fields(user)

    # After the call, width and height should still be None (not forced update)
    assert user.image_width is None
    assert user.image_height is None

    # Force the update of dimensions
    user.image.update_dimension_fields(user, force=True)

    # After forced call, width and height should be updated to actual image dimensions
    assert user.image_width is not None
    assert user.image_height is not None

    # Verify that the values are correct based on the test image
    assert user.image_width == image_file.width
    assert user.image_height == image_file.height

    # Set dimensions directly
    user.image_width = 100
    user.image_height = 200

    # Call again without force, should not change dimensions
    user.image.update_dimension_fields(user)

    assert user.image_width == 100
    assert user.image_height == 200

    # Set image to None and check update
    user.image.delete()
    user.image.update_dimension_fields(user)

    # After deleting image, dimensions should be cleared
    assert user.image_width is None
    assert user.image_height is None

    # Call with force should also clear dimensions
    user.image.update_dimension_fields(user, force=True)

    assert user.image_width is None
    assert user.image_height is None