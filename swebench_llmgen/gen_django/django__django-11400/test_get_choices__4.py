import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ForeignObjectRel

# A simplified ForeignObjectRel subclass for testing purposes
class TestForeignObjectRel(ForeignObjectRel):
    def __init__(self):
        self.related_model = User
        self.editable = True

# Test cases for get_choices method
def test_get_choices_includes_blank_choice():
    # Arrange
    rel = TestForeignObjectRel()
    expected_choices = [(BLANK_CHOICE_DASH[0], BLANK_CHOICE_DASH[1])] + [
        (user.pk, str(user)) for user in User.objects.all().order_by('username')
    ]

    # Act
    choices = rel.get_choices(include_blank=True)
    
    # Assert
    assert choices == expected_choices

def test_get_choices_excludes_blank_choice():
    # Arrange
    rel = TestForeignObjectRel()
    expected_choices = [
        (user.pk, str(user)) for user in User.objects.all().order_by('username')
    ]

    # Act
    choices = rel.get_choices(include_blank=False)
    
    # Assert
    assert choices == expected_choices

def test_get_choices_with_custom_ordering():
    # Arrange
    rel = TestForeignObjectRel()
    expected_choices = [
        (user.pk, str(user)) for user in User.objects.all().order_by('id')
    ]

    # Act
    choices = rel.get_choices(ordering=('id',))
    
    # Assert
    assert choices == expected_choices