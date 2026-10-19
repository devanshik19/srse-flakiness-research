import pytest
from django.db import models
from django.db.models import Q
from django.core.exceptions import FieldError
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.mark.parametrize(
    'filter_expr, branch_negated, current_negated, can_reuse, allow_joins, split_subq, check_filterable, expected_raise',
    [
        (('username', 'testuser'), False, False, None, True, True, True, None),
        (('username__exact', 'testuser'), False, False, None, True, True, True, None),
        (Q(username='testuser'), False, False, None, True, True, True, None),
        (None, False, False, None, True, True, True, FieldError),
        ({}, False, False, None, True, True, True, FieldError),
        (('username', None), False, False, None, True, True, True, FieldError),
    ]
)
def test_build_filter(filter_expr, branch_negated, current_negated, can_reuse, allow_joins, split_subq, check_filterable, expected_raise):
    query = Query(User)
    
    if expected_raise:
        with pytest.raises(expected_raise):
            query.build_filter(filter_expr, branch_negated, current_negated, can_reuse, allow_joins, split_subq, check_filterable)
    else:
        clause, used_joins = query.build_filter(filter_expr, branch_negated, current_negated, can_reuse, allow_joins, split_subq, check_filterable)
        assert clause is not None
        assert isinstance(clause, models.sql.where.WhereNode)