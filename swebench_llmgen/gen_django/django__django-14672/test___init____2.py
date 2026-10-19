import pytest
from django.contrib.auth.models import User
from django.db.models.fields.reverse_related import ForeignObjectRel

def test_foreign_object_rel_init():
    # Test with required parameters only
    field = 'some_field'
    to = User
    foreign_object_rel = ForeignObjectRel(field, to)

    assert foreign_object_rel.field == field
    assert foreign_object_rel.model == to
    assert foreign_object_rel.related_name is None
    assert foreign_object_rel.related_query_name is None
    assert foreign_object_rel.limit_choices_to == {}
    assert foreign_object_rel.parent_link is False
    assert foreign_object_rel.on_delete is None
    assert foreign_object_rel.symmetrical is False
    assert foreign_object_rel.multiple is True

    # Test with optional parameters
    related_name = 'related_user'
    related_query_name = 'related_user_query'
    limit_choices_to = {'is_active': True}
    parent_link = True
    on_delete = 'CASCADE'
    
    foreign_object_rel = ForeignObjectRel(field, to, related_name, related_query_name, limit_choices_to, parent_link, on_delete)

    assert foreign_object_rel.related_name == related_name
    assert foreign_object_rel.related_query_name == related_query_name
    assert foreign_object_rel.limit_choices_to == limit_choices_to
    assert foreign_object_rel.parent_link is True
    assert foreign_object_rel.on_delete == on_delete