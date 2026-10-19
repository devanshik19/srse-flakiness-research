import pytest
from django.contrib.auth.models import User
from django.db.models.fields.reverse_related import ForeignObjectRel

def test_foreign_object_rel_init():
    # Test Case 1: All parameters provided
    field = 'some_field'
    related_name = 'related_user'
    related_query_name = 'related_query'
    limit_choices_to = {'is_active': True}
    parent_link = True
    on_delete = 'CASCADE'
    
    foreign_object_rel = ForeignObjectRel(
        field,
        User,
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
    assert foreign_object_rel.parent_link is True
    assert foreign_object_rel.on_delete == on_delete
    assert foreign_object_rel.symmetrical is False
    assert foreign_object_rel.multiple is True

    # Test Case 2: limit_choices_to is None
    foreign_object_rel_none = ForeignObjectRel(
        field,
        User,
        related_name=related_name,
        limit_choices_to=None
    )
    
    assert foreign_object_rel_none.limit_choices_to == {}
    
    # Test Case 3: missing optional parameters
    foreign_object_rel_optional = ForeignObjectRel(
        field,
        User
    )
    
    assert foreign_object_rel_optional.related_name is None
    assert foreign_object_rel_optional.related_query_name is None
    assert foreign_object_rel_optional.limit_choices_to == {}
    assert foreign_object_rel_optional.parent_link is False
    assert foreign_object_rel_optional.on_delete is None