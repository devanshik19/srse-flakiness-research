import pytest
from django.contrib.auth.models import User
from django.db import models
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.db.models import ImageField

# Custom model to use the ImageField
class TestModel(models.Model):
    image = ImageField(upload_to='test_images/')
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)

# Test cases for the update_dimension_fields method
def test_update_dimension_fields_with_file():
    user = User.objects.create(username='testuser')
    test_model = TestModel.objects.create(image=ContentFile(b"image_data", name='test_image.jpg'))
    test_model.image = ImageFile(test_model.image)
    
    test_model.update_dimension_fields(test_model)

    assert test_model.width is not None
    assert test_model.height is not None

def test_update_dimension_fields_with_no_file():
    test_model = TestModel.objects.create(image=None)

    test_model.update_dimension_fields(test_model)

    assert test_model.width is None
    assert test_model.height is None

def test_update_dimension_fields_already_filled():
    user = User.objects.create(username='testuser')
    test_model = TestModel.objects.create(image=ContentFile(b"image_data", name='test_image.jpg'))
    test_model.image = ImageFile(test_model.image)
    
    # Initially populate width and height
    test_model.update_dimension_fields(test_model)

    # Now the values should not change if not forced
    width_before = test_model.width
    height_before = test_model.height

    test_model.update_dimension_fields(test_model)

    assert test_model.width == width_before
    assert test_model.height == height_before

def test_update_dimension_fields_force_update():
    user = User.objects.create(username='testuser')
    test_model = TestModel.objects.create(image=ContentFile(b"image_data", name='test_image.jpg'))
    test_model.image = ImageFile(test_model.image)
    
    test_model.update_dimension_fields(test_model)

    initial_width = test_model.width
    initial_height = test_model.height
    
    # Change the image (not actually changing the file here since we are focused on forced updates)
    test_model.image = ImageFile(test_model.image)

    # Force update
    test_model.update_dimension_fields(test_model, force=True)

    assert test_model.width == initial_width
    assert test_model.height == initial_height