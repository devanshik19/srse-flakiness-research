import pytest
from django.contrib.auth.models import User
from django.db import models


class ImageField(models.Field):
    attr_class = None
    descriptor_class = None
    description = "Image field"

    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        super().__init__(verbose_name, name, **kwargs)
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


class TestImageField:
    @pytest.fixture
    def user_with_image(self, db):
        user = User.objects.create(username='testuser')
        field = ImageField(width_field='image_width', height_field='image_height')
        setattr(user, 'image_file', ImageFile(File(open('path/to/image.jpg', 'rb'), 'image.jpg')))
        return user, field

    @pytest.fixture
    def user_without_image(self, db):
        user = User.objects.create(username='testuser2')
        field = ImageField(width_field='image_width', height_field='image_height')
        return user, field

    def test_update_dimension_fields_with_image(self, user_with_image):
        user, field = user_with_image
        user.image_width = None
        user.image_height = None
        field.update_dimension_fields(user)
        assert user.image_width is not None
        assert user.image_height is not None

    def test_update_dimension_fields_without_image(self, user_without_image):
        user, field = user_without_image
        user.image_width = None
        user.image_height = None
        field.update_dimension_fields(user)
        assert user.image_width is None
        assert user.image_height is None

    def test_does_not_update_if_dimensions_already_filled(self, user_with_image):
        user, field = user_with_image
        user.image_width = 100
        user.image_height = 200
        field.update_dimension_fields(user)
        assert user.image_width == 100
        assert user.image_height == 200

    def test_force_update_dimensions(self, user_with_image):
        user, field = user_with_image
        user.image_width = 100
        user.image_height = 200
        field.update_dimension_fields(user, force=True)
        assert user.image_width is not None
        assert user.image_height is not None