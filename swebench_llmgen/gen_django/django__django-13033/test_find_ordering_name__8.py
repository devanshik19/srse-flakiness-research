import pytest
from django.contrib.auth.models import User
from django.db.models import F, OrderBy
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query


@pytest.fixture
def sql_compiler():
    # Create a SQLCompiler instance for testing
    query = Query(model=User)  # Using User model
    return SQLCompiler(query=query, connection=None, using=None)


def test_find_ordering_name_field(sql_compiler):
    opts = User._meta  # Get the model options for User
    name = 'username'
    result = sql_compiler.find_ordering_name(name, opts)

    assert len(result) == 1
    assert isinstance(result[0], tuple)
    assert isinstance(result[0][0], OrderBy)
    assert result[0][0].expression.name == 'username'
    assert result[0][1] is False


def test_find_ordering_name_related_field(sql_compiler):
    # Create a User with a related profile model (assuming a related profile exists)
    opts = User._meta
    name = 'profile__bio'  # Assuming a 'bio' field exists on the related 'profile' model
    with pytest.raises(FieldError): 
        sql_compiler.find_ordering_name(name, opts)

  
def test_find_ordering_name_descending(sql_compiler):
    opts = User._meta
    name = 'username DESC'
    result = sql_compiler.find_ordering_name(name, opts)

    assert len(result) == 1
    assert result[0][0].descending is True


def test_find_ordering_name_with_infinite_loop(sql_compiler):
    opts = User._meta
    name = 'related__model__field'  # Modify as per your related field structure
    sql_compiler.query.alias_map[0] = type('Alias', (object,), {'join_cols': 'cols'})()
    
    # Simulate adding this join to already_seen
    sql_compiler.query.alias_map[1] = type('Alias', (object,), {'join_cols': 'cols'})()
    
    with pytest.raises(FieldError, match='Infinite loop caused by ordering.'):
        sql_compiler.find_ordering_name(name, opts, already_seen={('cols',)})