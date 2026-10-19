import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query

@pytest.mark.parametrize("combinator, all, expected_sql, expected_params", [
    ('union', False, 'SELECT * FROM (SELECT "auth_user"."id", "auth_user"."username" FROM "auth_user")', []),
    ('union', True, 'SELECT * FROM (SELECT "auth_user"."id", "auth_user"."username" FROM "auth_user") ALL', []),
    ('difference', False, 'SELECT * FROM (SELECT "auth_user"."id", "auth_user"."username" FROM "auth_user")', []),
])
def test_get_combinator_sql(combinator, all, expected_sql, expected_params):
    # Set up a query that selects some users
    query = Query(User.objects.all().only('id', 'username').query)
    connection = connections['default']
    compiler = SQLCompiler(query, connection, using='default')

    # Manually prepare combined queries with empty ones
    query.combined_queries = [query, query.none()]

    # Call the method
    result_sql, result_params = compiler.get_combinator_sql(combinator, all)

    # Check the SQL output
    assert result_sql[0].strip() == expected_sql.strip()
    assert result_params == expected_params

def test_get_combinator_sql_empty_result():
    query = Query(User.objects.none().query)
    connection = connections['default']
    compiler = SQLCompiler(query, connection, using='default')
    query.combined_queries = [query]

    with pytest.raises(EmptyResultSet):
        compiler.get_combinator_sql('union', False)