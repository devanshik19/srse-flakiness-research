import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query

@pytest.mark.parametrize("combinator, all, expected_exception", [
    ('union', False, None),
    ('difference', False, None),
    ('union', True, None),
    ('difference', True, None),
])
def test_get_combinator_sql(combinator, all, expected_exception):
    # Prepare a basic query for User model
    query1 = Query(User.objects.all())
    query2 = Query(User.objects.filter(is_active=True))

    # Combine the queries
    combined_queries = [query1, query2]

    # Mocking the basic structure to create SQLCompiler
    connection = connections['default']
    compiler = SQLCompiler(query=combined_queries[0], using='default', connection=connection)
    compiler.query.set_combined_queries(combined_queries)

    if expected_exception:
        with pytest.raises(expected_exception):
            compiler.get_combinator_sql(combinator, all)
    else:
        result, params = compiler.get_combinator_sql(combinator, all)
        assert isinstance(result, list)
        assert isinstance(params, list)
        assert len(result) > 0
        assert len(params) >= 0

def test_get_combinator_sql_empty_results():
    # Prepare an empty queryset
    query1 = Query(User.objects.none())
    query2 = Query(User.objects.filter(is_active=False))

    # Combine the empty query
    combined_queries = [query1, query2]

    connection = connections['default']
    compiler = SQLCompiler(query=combined_queries[0], using='default', connection=connection)
    compiler.query.set_combined_queries(combined_queries)

    with pytest.raises(EmptyResultSet):
        compiler.get_combinator_sql('union', False)