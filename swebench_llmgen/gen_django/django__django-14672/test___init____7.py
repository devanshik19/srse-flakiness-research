import pytest
from django.contrib.auth.models import User
from django.core import exceptions
from django.db.models.fields.reverse_related import ForeignObjectRel

def test_foreign_object_rel_init():
    # Test with all parameters provided
    field = 'some_field'
    related_name = 'related_users'
    related_query_name = 'user_query'
    limit_choices_to = {'is_active': True}
    parent_link = True
    on_delete = exceptions.PROTECT

    foreign_object_rel = ForeignObjectRel(
        field=field,
        to=User,
        related_name=related_name,
        related_query_name=related_query_name,
        limit_choices_to=limit_choices_to,
        parent_link=parent_link,
        on_delete=on_delete
    )

    assert foreign_object_rel.field == field
    assert foreign_object_rel.model == User
    assert foreign_object_rel.related_name == related_name
    assert foreign_object_rel.related_query_name == related_query_name
    assert foreign_object_rel.limit_choices_to == limit_choices_to
    assert foreign_object_rel.parent_link == parent_link
    assert foreign_object_rel.on_delete == on_delete
    assert foreign_object_rel.symmetrical is False
    assert foreign_object_rel.multiple is True

    # Test with the default values for optional parameters
    foreign_object_rel_default = ForeignObjectRel(field=field, to=User)

    assert foreign_object_rel_default.related_name is None
    assert foreign_object_rel_default.related_query_name is None
    assert foreign_object_rel_default.limit_choices_to == {}
    assert foreign_object_rel_default.parent_link is False
    assert foreign_object_rel_default.on_delete is None