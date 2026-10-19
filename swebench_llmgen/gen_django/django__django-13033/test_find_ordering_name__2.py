import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models import F, OrderBy


@pytest.mark.parametrize("name, expected_ordering", [
    ("username", [(OrderBy(F('username'), descending=False), False)]),
    ("username DESC", [(OrderBy(F('username'), descending=True), False)]),
    ("date_joined", [(OrderBy(F('date_joined'), descending=False), False)]),
    ("date_joined DESC", [(OrderBy(F('date_joined'), descending=True), False)]),
])
def test_find_ordering_name_basic(name, expected_ordering):
    compiler = SQLCompiler(None, None, None)
    opts = User._meta
    result = compiler.find_ordering_name(name, opts)
    assert result == expected_ordering


def test_find_ordering_name_infinite_loop():
    compiler = SQLCompiler(None, None, None)
    opts = User._meta
    alias = None
    name = "username"

    # Simulating a situation where it might cause an infinite loop
    compiler.query = type('Query', (), {'alias_map': {1: type('Alias', (), {'join_cols': (1,)})}})()
    with pytest.raises(FieldError, match='Infinite loop caused by ordering.'):
        compiler.find_ordering_name(name, opts, alias, 'ASC', already_seen={(1,)})