import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.db.models.fields.related import ForeignKey
from django.core.exceptions import FieldError

@pytest.mark.parametrize("name, expected", [
    ("username", [("username", False)]),
    ("date_joined", [("date_joined", False)]),
    ("profile__bio", [("profile__bio", False)]),
])
def test_find_ordering_name_single_field(name, expected):
    query = Query(User)
    compiler = SQLCompiler(query, connection, using='default')
    class MockOpts:
        ordering = ["username", "date_joined"]
        model = User
    opts = MockOpts()
    
    result = compiler.find_ordering_name(name, opts)
    assert len(result) == len(expected)
    for res, exp in zip(result, expected):
        assert res[0].get_source() == exp[0]
        assert res[1] == exp[1]

def test_find_ordering_name_with_related():
    query = Query(User)
    compiler = SQLCompiler(query, connection, using='default')
    
    class MockOpts:
        ordering = ["username", "profile__bio"]
    opts = MockOpts()

    with pytest.raises(FieldError, match='Infinite loop caused by ordering.'):
        compiler.find_ordering_name("profile__user__profile", opts)

def test_find_ordering_name_no_results():
    query = Query(User)
    compiler = SQLCompiler(query, connection, using='default')
    
    class MockOpts:
        ordering = []
        model = User
    opts = MockOpts()
    
    result = compiler.find_ordering_name("nonexistent_field", opts, default_order='ASC')
    assert result == []