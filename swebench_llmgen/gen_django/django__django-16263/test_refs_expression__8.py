import pytest
from django.contrib.auth.models import User
from django.db.models.constants import LOOKUP_SEP
from django.db.models.query_utils import refs_expression

def test_refs_expression_found():
    annotations = {
        'user__username': User.objects.create(username='testuser').username,
        'user__email': User.objects.create(username='test@example.com').email
    }
    lookup_parts = ['user', 'username']
    result, remaining = refs_expression(lookup_parts, annotations)
    assert result == annotations['user__username']
    assert remaining == []

def test_refs_expression_not_found():
    annotations = {
        'user__username': User.objects.create(username='testuser').username,
        'another_annotation': 'value'
    }
    lookup_parts = ['user', 'email']
    result, remaining = refs_expression(lookup_parts, annotations)
    assert result is False
    assert remaining == ('email',)

def test_refs_expression_partial_match():
    annotations = {
        'user': User.objects.create(username='testuser'),
        'user__username': User.objects.create(username='testuser2').username
    }
    lookup_parts = ['user']
    result, remaining = refs_expression(lookup_parts, annotations)
    assert result == annotations['user']
    assert remaining == []

def test_refs_expression_empty_lookup_parts():
    annotations = {
        'user__username': User.objects.create(username='testuser').username
    }
    lookup_parts = []
    result, remaining = refs_expression(lookup_parts, annotations)
    assert result is False
    assert remaining == ()