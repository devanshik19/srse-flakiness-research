import pytest
from django.contrib.auth.models import User
from django.db import models
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile

class ImageField(models.Field):
    attr_class = ImageFile
    descriptor_class = None
    description = "ImageField"
    
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **options):
        super().__init__(verbose_name, name, **options)
        self.width_field = width_field
        self.height_field = height_field
        
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

@pytest.fixture
def image_field():
    return ImageField(width_field='width', height_field='height')

@pytest.fixture
def user_with_image(image_field):
    user = User.objects.create(username='testuser')
    file_content = ContentFile(b"fake image content")  # Simulating an image
    image_file = ImageFile(file_content, name='test_image.jpg')

    setattr(user, image_field.attname, image_file)
    return user

def test_update_dimension_fields_no_file(image_field):
    user = User.objects.create(username='testuser')
    image_field.update_dimension_fields(user)
    assert getattr(user, image_field.width_field) is None
    assert getattr(user, image_field.height_field) is None

def test_update_dimension_fields_with_file(image_field, user_with_image):
    user = user_with_image
    user_with_image.save()  # Ensure the user is saved to get an ID
    
    # Simulate setting width and height
    setattr(user, image_field.attname, user_with_image.username)
    image_field.update_dimension_fields(user)

    # Assuming the fake image size is set for the test
    assert getattr(user, image_field.width_field) is not None
    assert getattr(user, image_field.height_field) is not None

def test_update_dimension_fields_force(image_field, user_with_image):
    user = user_with_image
    user.width = 100
    user.height = 200
    image_field.update_dimension_fields(user, force=True)
    
    # Assuming the fake image size is set for the test
    assert getattr(user, image_field.width_field) == user_with_image.width
    assert getattr(user, image_field.height_field) == user_with_image.height

def test_update_dimension_fields_already_filled(image_field):
    user = User.objects.create(username='testuser')
    setattr(user, image_field.width_field, 400)
    setattr(user, image_field.height_field, 300)

    image_field.update_dimension_fields(user)
    
    assert getattr(user, image_field.width_field) == 400
    assert getattr(user, image_field.height_field) == 300