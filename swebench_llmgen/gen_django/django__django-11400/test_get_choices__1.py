import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from django.core import exceptions
from django.utils.functional import cached_property

class ForeignObjectRel:
    def __init__(self, field, to, related_name, related_query_name, limit_choices_to=None, parent_link=False, on_delete=models.CASCADE):
        self.field = field
        self.to = to
        self.related_name = related_name
        self.related_query_name = related_query_name
        self.limit_choices_to = limit_choices_to
        self.parent_link = parent_link
        self.on_delete = on_delete
        self.related_model = to

    def get_choices(self, include_blank=True, blank_choice='', ordering=()):
        return (blank_choice if include_blank else []) + [
            (x.pk, str(x)) for x in self.related_model._default_manager.order_by(*ordering)
        ]

@pytest.mark.django_db
def test_get_choices_with_blank():
    rel = ForeignObjectRel(field=ForeignKey(User, on_delete=models.CASCADE), 
                           to=User,
                           related_name='related_users', 
                           related_query_name='related_user')

    # Create user instances for testing
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    choices = rel.get_choices(include_blank=True, blank_choice='Select a user')
    assert len(choices) == 3  # 1 blank choice + 2 user choices
    assert choices[0] == ('Select a user', 'Select a user')
    assert choices[1] == (user1.pk, str(user1))
    assert choices[2] == (user2.pk, str(user2))

@pytest.mark.django_db
def test_get_choices_without_blank():
    rel = ForeignObjectRel(field=ForeignKey(User, on_delete=models.CASCADE), 
                           to=User,
                           related_name='related_users', 
                           related_query_name='related_user')

    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    choices = rel.get_choices(include_blank=False)
    assert len(choices) == 2  # Only user choices should be present
    assert choices[0] == (user1.pk, str(user1))
    assert choices[1] == (user2.pk, str(user2))

@pytest.mark.django_db
def test_get_choices_ordering():
    rel = ForeignObjectRel(field=ForeignKey(User, on_delete=models.CASCADE), 
                           to=User,
                           related_name='related_users', 
                           related_query_name='related_user')

    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')

    # Test ordering by username
    choices = rel.get_choices(ordering=['username'])
    assert choices[0] == (user1.pk, str(user1))
    assert choices[1] == (user2.pk, str(user2))
    assert choices[2] == (user3.pk, str(user3))