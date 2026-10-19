import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models.expressions import Col
from django.db.models.sql.where import WhereNode

@pytest.fixture
def query():
    # Create a dummy Query object with minimal setup
    model = User
    q = Query(model=model, alias_cols=())
    q.alias_map = {'old_alias': q.get_initial_alias()}
    q.alias_refcount = {'old_alias': 1}
    q.external_aliases = {'old_alias': False}
    q.select = (Col('username'),)
    q.group_by = (Col('email'),)
    q.where = WhereNode()
    return q

def test_change_aliases(query):
    change_map = {'old_alias': 'new_alias'}
    
    # Prepare internal structures
    query.alias_map['old_alias'] = query.get_initial_alias()
    query.alias_refcount['old_alias'] = 1
    query.table_map = {query.alias_map['old_alias']: ['old_alias']}

    # Execute the method
    query.change_aliases(change_map)

    # Assertions
    assert 'new_alias' in query.alias_map
    assert 'old_alias' not in query.alias_map
    assert query.select == (Col('username'),)
    assert query.group_by == (Col('email'),)
    assert query.alias_refcount['new_alias'] == 1
    assert query.external_aliases['new_alias'] is True

    # Check if the where clause can also reflect changes
    assert query.where.get_children() == []

    # Check if aliases in select are correctly relabeled
    relabeled_select = query.select[0].relabeled_clone(change_map)
    assert relabeled_select.alias == 'username'