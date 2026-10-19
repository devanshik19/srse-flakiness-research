import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.reverse_related import ForeignObjectRel

class MyModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

@pytest.fixture
def foreign_object_rel():
    return ForeignObjectRel(field=MyModel.user.field, to='auth.User', related_name='my_models', related_query_name='my_model')

def test_get_choices_with_blank(foreign_object_rel):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    choices = foreign_object_rel.get_choices(include_blank=True)
    expected_choices = [(BLANK_CHOICE_DASH[0], BLANK_CHOICE_DASH[1])] + [
        (user1.pk, str(user1)),
        (user2.pk, str(user2)),
    ]
    
    assert choices == expected_choices

def test_get_choices_without_blank(foreign_object_rel):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    choices = foreign_object_rel.get_choices(include_blank=False)
    expected_choices = [
        (user1.pk, str(user1)),
        (user2.pk, str(user2)),
    ]
    
    assert choices == expected_choices

def test_get_choices_with_ordering(foreign_object_rel):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')

    choices = foreign_object_rel.get_choices(ordering=['username'])
    expected_choices = [
        (user1.pk, str(user1)),
        (user2.pk, str(user2)),
        (user3.pk, str(user3)),
    ]
    
    assert choices == expected_choices