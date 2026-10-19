import pytest
from django.contrib.auth.models import User
from django.core import exceptions
from django.db.models.fields.reverse_related import ForeignObjectRel

def test_foreign_object_rel_init():
    # Test initialization with required parameters
    rel = ForeignObjectRel(field='some_field', to=User)
    assert rel.field == 'some_field'
    assert rel.model == User
    assert rel.related_name is None
    assert rel.related_query_name is None
    assert rel.limit_choices_to == {}
    assert rel.parent_link is False
    assert rel.on_delete is None
    assert rel.symmetrical is False
    assert rel.multiple is True

    # Test initialization with all parameters
    custom_limit_choices_to = {'is_active': True}
    rel_full = ForeignObjectRel(
        field='some_field',
        to=User,
        related_name='related_user',
        related_query_name='related_user_query',
        limit_choices_to=custom_limit_choices_to,
        parent_link=True,
        on_delete=exceptions.PROTECT
    )
    assert rel_full.field == 'some_field'
    assert rel_full.model == User
    assert rel_full.related_name == 'related_user'
    assert rel_full.related_query_name == 'related_user_query'
    assert rel_full.limit_choices_to == custom_limit_choices_to
    assert rel_full.parent_link is True
    assert rel_full.on_delete == exceptions.PROTECT
    assert rel_full.symmetrical is False
    assert rel_full.multiple is True