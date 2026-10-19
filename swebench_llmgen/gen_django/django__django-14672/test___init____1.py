import pytest
from django.contrib.auth.models import User
from django.db.models.fields.reverse_related import ForeignObjectRel

def test_foreign_object_rel_init_with_all_params():
    field = 'my_field'
    to = User
    related_name = 'my_related_name'
    related_query_name = 'my_related_query_name'
    limit_choices_to = {'is_active': True}
    parent_link = True
    on_delete = None
    
    relation = ForeignObjectRel(
        field,
        to,
        related_name,
        related_query_name,
        limit_choices_to,
        parent_link,
        on_delete
    )
    
    assert relation.field == field
    assert relation.model == to
    assert relation.related_name == related_name
    assert relation.related_query_name == related_query_name
    assert relation.limit_choices_to == limit_choices_to
    assert relation.parent_link == parent_link
    assert relation.on_delete == on_delete
    assert relation.symmetrical is False
    assert relation.multiple is True

def test_foreign_object_rel_init_with_defaults():
    field = 'another_field'
    to = User
    
    relation = ForeignObjectRel(field, to)
    
    assert relation.field == field
    assert relation.model == to
    assert relation.related_name is None
    assert relation.related_query_name is None
    assert relation.limit_choices_to == {}
    assert relation.parent_link is False
    assert relation.on_delete is None
    assert relation.symmetrical is False
    assert relation.multiple is True