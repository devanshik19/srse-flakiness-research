import pytest
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

def test_resolve_expression():
    # Create sample users for testing
    user1 = User.objects.create_user(username='user1', password='pass')
    user2 = User.objects.create_user(username='user2', password='pass')

    # Create a QuerySet
    queryset = User.objects.all()

    # Create an instance of Q
    q_instance = Q(username='user1')

    # Call resolve_expression
    clause = q_instance.resolve_expression(query=queryset)

    # Verify the clause generated
    assert isinstance(clause, QuerySet)

    # Check if the clause actually filters correctly
    filtered_users = list(queryset.filter(clause))
    assert len(filtered_users) == 1
    assert filtered_users[0].username == user1.username

    # Test allowing joins
    clause_with_joins = q_instance.resolve_expression(query=queryset, allow_joins=True)
    assert isinstance(clause_with_joins, QuerySet)

    # Test with summarize flag
    clause_summarize = q_instance.resolve_expression(query=queryset, summarize=True)
    assert isinstance(clause_summarize, QuerySet)

    # Test with for_save flag
    clause_for_save = q_instance.resolve_expression(query=queryset, for_save=True)
    assert isinstance(clause_for_save, QuerySet)

    # Test with reuse flag
    clause_reuse = q_instance.resolve_expression(query=queryset, reuse=None)
    assert isinstance(clause_reuse, QuerySet)