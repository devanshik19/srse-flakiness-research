import pytest
from django.contrib.auth.models import User
from django.db import models

# Assuming ForeignObjectRel is a part of a relevant class that we can instantiate
class ForeignObjectRel:
    # Initialization and other methods omitted for brevity

    def __init__(self, related_model):
        self.related_model = related_model

    def get_choices(self, include_blank=True, blank_choice='---------', ordering=()):
        return (blank_choice if include_blank else []) + [
            (x.pk, str(x)) for x in self.related_model._default_manager.order_by(*ordering)
        ]

@pytest.mark.django_db
def test_get_choices_with_blank():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    foreign_object_rel = ForeignObjectRel(related_model=User)
    
    choices = foreign_object_rel.get_choices()
    
    assert choices[0] == ('---------', '---------')  # Blank choice
    assert (user1.pk, str(user1)) in choices
    assert (user2.pk, str(user2)) in choices

@pytest.mark.django_db
def test_get_choices_without_blank():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    foreign_object_rel = ForeignObjectRel(related_model=User)
    
    choices = foreign_object_rel.get_choices(include_blank=False)
    
    assert choices == [(user1.pk, str(user1)), (user2.pk, str(user2))]

@pytest.mark.django_db
def test_get_choices_with_ordering():
    user1 = User.objects.create(username='user2')
    user2 = User.objects.create(username='user1')
    
    foreign_object_rel = ForeignObjectRel(related_model=User)
    
    choices = foreign_object_rel.get_choices(ordering=['username'])

    assert choices[0] == ('---------', '---------')  # Blank choice
    assert choices[1] == (user2.pk, str(user2))  # user1 comes first alphabetically
    assert choices[2] == (user1.pk, str(user1))