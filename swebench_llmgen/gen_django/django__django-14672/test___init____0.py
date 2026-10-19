import pytest
from django.contrib.auth.models import User
from django.core import exceptions
from django.db.models.fields.reverse_related import ForeignObjectRel

def test_foreign_object_rel_init():
    # Test case for initializing ForeignObjectRel with all parameters
    field = 'example_field'
    to = User
    related_name = 'related_users'
    related_query_name = 'user_query'
    limit_choices_to = {'is_active': True}
    parent_link = True
    on_delete = None
    
    foreign_object_rel = ForeignObjectRel(field, to, related_name, related_query_name,
                                          limit_choices_to, parent_link, on_delete)

    assert foreign_object_rel.field == field
    assert foreign_object_rel.model == to
    assert foreign_object_rel.related_name == related_name
    assert foreign_object_rel.related_query_name == related_query_name
    assert foreign_object_rel.limit_choices_to == limit_choices_to
    assert foreign_object_rel.parent_link is True
    assert foreign_object_rel.on_delete is None
    assert foreign_object_rel.symmetrical is False
    assert foreign_object_rel.multiple is True

    # Test case for initializing ForeignObjectRel with default parameters
    foreign_object_rel_default = ForeignObjectRel(field, to)

    assert foreign_object_rel_default.field == field
    assert foreign_object_rel_default.model == to
    assert foreign_object_rel_default.related_name is None
    assert foreign_object_rel_default.related_query_name is None
    assert foreign_object_rel_default.limit_choices_to == {}
    assert foreign_object_rel_default.parent_link is False
    assert foreign_object_rel_default.on_delete is None
    assert foreign_object_rel_default.symmetrical is False
    assert foreign_object_rel_default.multiple is True