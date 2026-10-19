import pytest
from django.contrib.auth.models import User
from django.db.models.fields.reverse_related import ForeignObjectRel


def test_foreign_object_rel_init():
    # Test with required parameters
    foreign_object_rel = ForeignObjectRel(field='test_field', to=User)
    assert foreign_object_rel.field == 'test_field'
    assert foreign_object_rel.model == User
    assert foreign_object_rel.related_name is None
    assert foreign_object_rel.related_query_name is None
    assert foreign_object_rel.limit_choices_to == {}
    assert foreign_object_rel.parent_link is False
    assert foreign_object_rel.on_delete is None
    assert foreign_object_rel.symmetrical is False
    assert foreign_object_rel.multiple is True

    # Test with additional parameters
    limit_choices = {'is_active': True}
    foreign_object_rel = ForeignObjectRel(field='test_field', to=User, related_name='users', 
                                          related_query_name='user_query', limit_choices_to=limit_choices, 
                                          parent_link=True, on_delete='CASCADE')
    assert foreign_object_rel.related_name == 'users'
    assert foreign_object_rel.related_query_name == 'user_query'
    assert foreign_object_rel.limit_choices_to == limit_choices
    assert foreign_object_rel.parent_link is True
    assert foreign_object_rel.on_delete == 'CASCADE'