import operator
from functools import reduce
from django.core.exceptions import EmptyResultSet, FullResultSet
from django.db.models.expressions import Case, When
from django.db.models.lookups import Exact
from django.utils import tree
from django.utils.functional import cached_property
from django.contrib.auth.models import User
from django.db.models.sql.where import WhereNode

def test_as_sql():
    # Create a WhereNode instance with various conditions
    user_condition = Exact('username', 'test_user')
    user_condition2 = Exact('email', 'test@example.com')

    # Normal conditions
    node = WhereNode([user_condition, user_condition2], connector='AND')
    
    # Compiler and connection context
    class MockCompiler:
        def compile(self, condition):
            if condition == user_condition:
                return ("username = %s", ['test_user'])
            elif condition == user_condition2:
                return ("email = %s", ['test@example.com'])
            raise EmptyResultSet
    
    class MockConnection:
        features = type('MockFeatures', (), {'supports_logical_xor': True})

    compiler = MockCompiler()
    connection = MockConnection()

    # Test normal scenario
    sql, params = node.as_sql(compiler, connection)
    assert sql == "(username = %s AND email = %s)"
    assert params == ['test_user', 'test@example.com']

    # Test with no conditions (EmptyResultSet)
    empty_node = WhereNode([], connector='AND')
    with pytest.raises(EmptyResultSet):
        empty_node.as_sql(compiler, connection)

    # Test with negation
    negated_node = WhereNode([user_condition], connector='AND', negated=True)
    sql_negated, params_negated = negated_node.as_sql(compiler, connection)
    assert sql_negated == "NOT (username = %s)"
    assert params_negated == ['test_user']

    # Full Result Set case
    full_condition_node = WhereNode([user_condition], connector='AND', negated=False)
    assert full_condition_node.as_sql(compiler, connection) == ("(username = %s)", ['test_user'])

    # Test XOR reduction for unsupported feature
    unsupported_xor_node = WhereNode([user_condition, user_condition2], connector='XOR')
    sql_xor, params_xor = unsupported_xor_node.as_sql(compiler, connection)
    assert sql_xor.startswith('(')  # should wrap in parentheses due to XOR conversion