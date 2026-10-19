import pytest
from django.contrib.auth.models import User
from django.db import models


class ImageField(models.Field):  # Simulating ImageField for the test
    attr_class = None
    descriptor_class = None
    description = "ImageField"
    
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        self.verbose_name = verbose_name
        self.name = name
        self.width_field = width_field
        self.height_field = height_field
        super().__init__(**kwargs)

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


class TestImageField(models.Model):
    image = ImageField(width_field='width', height_field='height')
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)


@pytest.mark.usefixtures('django_db_setup')
def test_update_dimension_fields():
    user = User.objects.create(username='testuser')
    test_instance = TestImageField.objects.create(image=None)

    # Test: No file and not forced
    test_instance.image = None
    test_instance.update_dimension_fields(test_instance)
    assert test_instance.width is None
    assert test_instance.height is None

    # Test: No file but forced
    test_instance.update_dimension_fields(test_instance, force=True)
    assert test_instance.width is None
    assert test_instance.height is None
    
    # Simulate ImageFieldFile behavior
    class MockImageFile:
        width = 100
        height = 200
    
    test_instance.image = MockImageFile()
    
    # Test: Update dimensions with file present
    test_instance.update_dimension_fields(test_instance)
    assert test_instance.width == 100
    assert test_instance.height == 200

    # Test: Already filled dimensions, no force
    test_instance.width = 50
    test_instance.height = 50
    test_instance.update_dimension_fields(test_instance)
    assert test_instance.width == 50
    assert test_instance.height == 50

    # Test: Force update with filled dimensions
    test_instance.update_dimension_fields(test_instance, force=True)
    assert test_instance.width == 100
    assert test_instance.height == 200