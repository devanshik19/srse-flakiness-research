import pytest
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.sql.compiler import SQLCompiler
from django.db.models import QuerySet


@pytest.mark.parametrize("name, expected", [
    # Testing simple field ordering
    ('username', [('username', False)]),
    ('-username', [('username', True)]),
    # Testing related field ordering
    ('first_name__username', [('first_name', False)]),  # assuming first_name is related
    ('-first_name__username', [('first_name', True)]),
    # Testing ambiguous ordering names
    ('last_name', [('last_name', False)]),
    ('-last_name', [('last_name', True)]),
])
def test_find_ordering_name(name, expected):
    opts = User._meta
    compiler = SQLCompiler(QuerySet(User).query, None, None)  # emulate the compiler context
    actual = compiler.find_ordering_name(name, opts)

    assert len(actual) == len(expected)
    for (order_by, order_desc), (expected_field, expected_desc) in zip(actual, expected):
        assert order_by.field.name == expected_field
        assert order_desc == expected_desc