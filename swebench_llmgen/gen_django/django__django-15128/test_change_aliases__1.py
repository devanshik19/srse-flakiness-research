import pytest
from django.db.models.sql.query import Query
from django.contrib.auth.models import User
from django.db.models.expressions import F

@pytest.fixture
def query_instance():
    # Create a Query instance with select columns, where clause, and alias_map configurations.
    user = User.objects.create(username="testuser", email="test@example.com")
    instance = Query(model=User, alias_cols=(F('id'),))
    instance.select = (F('username'),)
    instance.where = instance.build_where(Q(username='testuser'))
    instance.alias_map = {
        'user_alias': instance.base_table(),
    }
    instance.alias_refcount = {
        'user_alias': 1,
    }
    instance.external_aliases = {
        'user_alias': False,
    }
    return instance

def test_change_aliases(query_instance):
    change_map = {
        'user_alias': 'new_user_alias',
    }
    query_instance.change_aliases(change_map)

    # Assertions to verify the behavior of change_aliases
    assert 'new_user_alias' in query_instance.alias_map
    assert 'user_alias' not in query_instance.alias_map
    assert query_instance.alias_refcount['new_user_alias'] == 1
    assert 'user_alias' not in query_instance.alias_refcount
    
    # Check if select has updated aliases
    assert len(query_instance.select) == 1  # Ensure we still have the right columns
    assert query_instance.where.clauses == [('username', 'testuser')]

    # Validate the external_aliases update
    assert 'new_user_alias' in query_instance.external_aliases
    assert query_instance.external_aliases['new_user_alias'] is False