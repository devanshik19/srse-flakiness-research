import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query

def test_find_ordering_name():
    # Create a mock query and a SQLCompiler instance
    query = Query(User)
    compiler = SQLCompiler(query, None, None)

    # Prepare options for the function
    opts = User._meta

    # Test cases for ordering names
    ordering_name_asc = 'username'
    ordering_name_desc = 'username__desc'
    ambiguous_ordering_name = 'first_name'

    # Test ascending ordering
    result_asc = compiler.find_ordering_name(ordering_name_asc, opts)
    assert len(result_asc) == 1
    assert result_asc[0][0].expression.name == 'username'
    assert result_asc[0][0].descending is False

    # Test descending ordering
    result_desc = compiler.find_ordering_name(ordering_name_desc, opts)
    assert len(result_desc) == 1
    assert result_desc[0][0].expression.name == 'username'
    assert result_desc[0][0].descending is True

    # Test handling of ambiguous names (e.g., relationships)
    with pytest.raises(FieldError):
        # Assuming an ambiguous scenario occurs for this test
        compiler.find_ordering_name(ambiguous_ordering_name, opts, already_seen=set())