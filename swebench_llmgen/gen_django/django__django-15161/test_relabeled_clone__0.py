import pytest
from django.db.models import expressions
from django.contrib.auth.models import User


@pytest.mark.parametrize("change_map, expected_ids", [
    ({}, [1]),  # No changes
    ({'id': 'user_id'}, ['user_id']),  # Change id to user_id
    ({'username': 'user_name'}, ['user_name']),  # Change username to user_name
])
def test_relabeled_clone(change_map, expected_ids):
    # Create an instance of BaseExpression
    expr = expressions.BaseExpression(output_field=None)
    
    # Mocking the required methods for the test
    def mock_get_source_expressions():
        return [User(pk) for pk in expected_ids]

    expr.get_source_expressions = mock_get_source_expressions
    expr.copy = lambda: expressions.BaseExpression(output_field=None)
    expr.set_source_expressions = lambda exprs: None
    
    # Perform relabeled_clone
    cloned_expr = expr.relabeled_clone(change_map)
    
    # Verify if the source expressions were updated as expected
    assert cloned_expr.get_source_expressions() == [User(pk) for pk in expected_ids]