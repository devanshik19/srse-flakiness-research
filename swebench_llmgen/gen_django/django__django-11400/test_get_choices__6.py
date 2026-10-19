import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from django.core import exceptions
from django.utils.functional import cached_property
from . import BLANK_CHOICE_DASH
from .mixins import FieldCacheMixin

class ForeignObjectRel:
    def __init__(self, field, to, related_name, related_query_name, limit_choices_to, parent_link, on_delete):
        self.field = field
        self.to = to
        self.related_name = related_name
        self.related_query_name = related_query_name
        self.limit_choices_to = limit_choices_to
        self.parent_link = parent_link
        self.on_delete = on_delete
        self.auto_created = False
        self.concrete = True
        self.editable = True
        self.is_relation = True
        self.null = True

    @cached_property
    def related_model(self):
        return self.to

    def get_choices(self, include_blank=True, blank_choice=BLANK_CHOICE_DASH, ordering=()):
        return (blank_choice if include_blank else []) + [
            (x.pk, str(x)) for x in self.related_model._default_manager.order_by(*ordering)
        ]

@pytest.fixture
def foreign_object_rel():
    return ForeignObjectRel(
        field=None,
        to=User,
        related_name='test_related',
        related_query_name='test_related_query',
        limit_choices_to=None,
        parent_link=False,
        on_delete=models.CASCADE
    )

def test_get_choices_includes_blank(foreign_object_rel):
    choices = foreign_object_rel.get_choices()
    assert choices[0] == BLANK_CHOICE_DASH
    assert len(choices) > 1  # Ensure there is at least one user choice

def test_get_choices_no_blank(foreign_object_rel):
    choices = foreign_object_rel.get_choices(include_blank=False)
    assert choices[0] != BLANK_CHOICE_DASH
    assert len(choices) > 0  # Ensure there is at least one user choice

def test_get_choices_ordering(foreign_object_rel):
    User.objects.create(username='user1')
    User.objects.create(username='user2')
    choices = foreign_object_rel.get_choices(ordering=['username'])
    assert choices[1][1] == 'user1'
    assert choices[2][1] == 'user2'