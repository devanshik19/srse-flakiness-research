import pytest
from django.contrib.auth.models import User
from django.db import models

class ImageField(models.Field):
    attr_class = 'ImageFieldFile'  # Placeholder for actual implementation
    descriptor_class = 'ImageFileDescriptor'  # Placeholder for actual implementation
    description = "An image field"

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
            (self.width_field and not getattr(instance, self.width_field)) or
            (self.height_field and not getattr(instance, self.height_field))
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

@pytest.mark.django_db
def test_update_dimension_fields():
    # Create a user instance
    user = User.objects.create_user(username='testuser', password='testpass')

    # Create an instance of ImageField with dimension fields
    image_field = ImageField(width_field='image_width', height_field='image_height')
    
    # Simulate attaching the image_field to the user model
    user.image_field = None  # Simulating no file initially
    image_field.attname = 'image_field'
    
    # Test without forcing and no file
    image_field.update_dimension_fields(user)
    assert user.image_width is None
    assert user.image_height is None

    # Simulate setting a file with dimensions
    class DummyImage:
        width = 100
        height = 200
    
    user.image_field = DummyImage()  # This simulates that the instance has an image file
    image_field.update_dimension_fields(user)
    assert user.image_width == 100
    assert user.image_height == 200

    # Test when dimensions are already filled
    user.image_width = 150
    user.image_height = 250
    image_field.update_dimension_fields(user)
    assert user.image_width == 150
    assert user.image_height == 250

    # Force the update
    image_field.update_dimension_fields(user, force=True)
    assert user.image_width == 100
    assert user.image_height == 200

    # Clear the file and check if dimensions clear
    user.image_field = None
    image_field.update_dimension_fields(user)
    assert user.image_width is None
    assert user.image_height is None