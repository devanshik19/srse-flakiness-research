import pytest
from django.contrib.auth.models import User
from django.core import exceptions
from django.db.models.fields.reverse_related import ForeignObjectRel

def test_foreign_object_rel_init():
    # Test default initialization
    rel = ForeignObjectRel(field='user_field', to=User)
    assert rel.field == 'user_field'
    assert rel.model == User
    assert rel.related_name is None
    assert rel.related_query_name is None
    assert rel.limit_choices_to == {}
    assert rel.parent_link is False
    assert rel.on_delete is None
    assert rel.symmetrical is False
    assert rel.multiple is True

    # Test initialization with all parameters
    limit_choices = {'is_active': True}
    rel_full = ForeignObjectRel(
        field='profile_field',
        to=User,
        related_name='profiles',
        related_query_name='profile',
        limit_choices_to=limit_choices,
        parent_link=True,
        on_delete='CASCADE'
    )
    assert rel_full.field == 'profile_field'
    assert rel_full.model == User
    assert rel_full.related_name == 'profiles'
    assert rel_full.related_query_name == 'profile'
    assert rel_full.limit_choices_to == limit_choices
    assert rel_full.parent_link is True
    assert rel_full.on_delete == 'CASCADE'
    assert rel_full.symmetrical is False
    assert rel_full.multiple is True