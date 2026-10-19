import pytest
from django.db.models.sql.query import Query
from django.contrib.auth.models import User

@pytest.fixture
def setup_query():
    model = User
    query = Query(model)
    return query

def test_trim_start(setup_query):
    query = setup_query
    # Simulating the names_with_path structure
    names_with_path = [
        ('related_name_1', [{'m2m': False, 'join_field': User._meta.get_field('id')}]),
        ('related_name_2', [{'m2m': True, 'join_field': User._meta.get_field('username')}])
    ]

    trimmed_prefix, contains_louter = query.trim_start(names_with_path)
    
    assert trimmed_prefix == ['related_name_1', 'username']
    assert not contains_louter

    # Testing a scenario with LEFT OUTER join
    names_with_path_louter = [
        ('related_name_1', [{'m2m': False, 'join_field': User._meta.get_field('id')}]),
        ('related_name_2', [{'m2m': False, 'join_field': User._meta.get_field('email')}])
    ]

    # Simulating that the second path is a LEFT OUTER join
    query.alias_map = {'alias_1': 'base_table', 'alias_2': 'base_table'}
    query.alias_map['alias_2'].join_type = LOUTER
    
    trimmed_prefix_louter, contains_louter = query.trim_start(names_with_path_louter)
    
    assert trimmed_prefix_louter == ['related_name_1', 'email']
    assert contains_louter