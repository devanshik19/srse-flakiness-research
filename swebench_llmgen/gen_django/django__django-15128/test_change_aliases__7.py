import pytest
from django.db.models import QuerySet
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def user_queryset():
    return User.objects.all()

def test_change_aliases(user_queryset):
    query = Query(User, alias_cols=())
    original_alias_map = {'u1': 'user1', 'u2': 'user2'}
    new_alias_map = {'user1': 'u1', 'user2': 'u2'}

    # Preparing the state before testing
    query.alias_map = {alias: None for alias in original_alias_map.values()}
    query.alias_refcount = {alias: 1 for alias in original_alias_map.values()}
    query.select = (Col('username', alias='u1'), Col('email', alias='u2'))
    query.where = WhereNode()  # Assuming it can be constructed like this
    query.external_aliases = {'user1': False, 'user2': False}
    query.group_by = (Col('username', alias='u1'),)

    # Perform change aliases
    query.change_aliases(new_alias_map)

    # Validate aliases in select, where, and external_aliases
    assert all(col.alias in new_alias_map.values() for col in query.select)
    assert query.group_by == tuple(Col('username', alias='u1').relabeled_clone(new_alias_map),)
    assert query.external_aliases == {
        'u1': True,
        'u2': True
    }
    
    # Validate alias_map and alias_refcount
    assert 'u1' in query.alias_map
    assert 'u2' in query.alias_map
    assert query.alias_refcount['u1'] == 1
    assert query.alias_refcount['u2'] == 1
    assert 'user1' not in query.alias_map
    assert 'user2' not in query.alias_map