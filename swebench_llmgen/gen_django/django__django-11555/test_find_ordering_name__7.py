import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models import F
from django.db.models.sql.query import Query

@pytest.fixture
def sql_compiler():
    query = Query(User)
    connection = None  # Replace with the actual connection if needed
    return SQLCompiler(query, connection, using=None)

def test_find_ordering_name_ascending(sql_compiler):
    result = sql_compiler.find_ordering_name('username', User._meta, default_order='ASC')
    assert len(result) == 1
    assert result[0][0].expression.name == 'username'
    assert result[0][0].descending is False

def test_find_ordering_name_descending(sql_compiler):
    result = sql_compiler.find_ordering_name('username__desc', User._meta, default_order='ASC')
    assert len(result) == 1
    assert result[0][0].expression.name == 'username'
    assert result[0][0].descending is True

def test_find_ordering_name_with_relation(sql_compiler):
    # Assuming there is a ForeignKey relation, e.g., User has a ForeignKey to a Profile model
    # You can adjust the name as necessary based on actual relations in your model
    # For this test case, let's assume there's a related field 'profile__bio'
    result = sql_compiler.find_ordering_name('profile__bio', User._meta, default_order='ASC')
    assert len(result) == 1
    assert result[0][0].expression.name == 'bio'

def test_find_ordering_name_infinite_loop(sql_compiler):
    sql_compiler.query.alias_map['infinite_join'] = SQLCompiler(query=Query(User))
    sql_compiler.query.alias_map['infinite_join'].join_cols = ['username']
    
    with pytest.raises(FieldError, match='Infinite loop caused by ordering.'):
        sql_compiler.find_ordering_name('infinite_join__username', User._meta, already_seen=set())