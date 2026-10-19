import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models import F, Value
from django.db.models.expressions import OrderBy
from django.db.models.sql.constants import LOOKUP_SEP
from django.db.models import OuterRef

@pytest.fixture
def sql_compiler():
    # Creates an instance of SQLCompiler
    return SQLCompiler(None, None, None)

def test_find_ordering_name_single_field(sql_compiler):
    user_model_opts = User._meta
    result = sql_compiler.find_ordering_name('username', user_model_opts)
    expected = [(OrderBy(F('username'), descending=False), False)]
    assert result == expected

def test_find_ordering_name_descending(sql_compiler):
    user_model_opts = User._meta
    result = sql_compiler.find_ordering_name('username__desc', user_model_opts)
    expected = [(OrderBy(F('username'), descending=True), False)]
    assert result == expected

def test_find_ordering_name_multiple_fields(sql_compiler):
    user_model_opts = User._meta
    result = sql_compiler.find_ordering_name('first_name__last_name', user_model_opts)
    expected = [(OrderBy(F('first_name'), descending=False), False),
                (OrderBy(F('last_name'), descending=False), False)]
    assert result == expected

def test_find_ordering_name_relation(sql_compiler):
    class CustomUser(User):
        class Meta:
            ordering = ['date_joined']

    custom_user_opts = CustomUser._meta
    result = sql_compiler.find_ordering_name('date_joined', custom_user_opts)
    expected = [(OrderBy(F('date_joined'), descending=False), False)]
    assert result == expected

def test_find_ordering_name_infinite_loop(sql_compiler):
    user_model_opts = User._meta
    # Simulate a situation where an infinite loop would occur
    sql_compiler.query = OuterRef('user')  # Mocking join-like behavior
    with pytest.raises(FieldError, match='Infinite loop caused by ordering.'):
        sql_compiler.find_ordering_name('username__username', user_model_opts)

def test_find_ordering_name_with_default_order(sql_compiler):
    user_model_opts = User._meta
    result = sql_compiler.find_ordering_name('username', user_model_opts, default_order='DESC')
    expected = [(OrderBy(F('username'), descending=True), False)]
    assert result == expected