import pytest
from django.contrib.auth.models import User
from django.db.models.constants import LOOKUP_SEP
from django.core.exceptions import FieldError
from django.db import DatabaseError, connections
from django.db.models.query_utils import refs_expression

def test_refs_expression_found():
    lookup_parts = ['username', 'profile', 'bio']
    annotations = {
        'username': User.objects.first().username,
        'username.profile': User.objects.first().profile,
        'username.profile.bio': 'Sample bio'
    }
    result, remaining = refs_expression(lookup_parts, annotations)
    assert result == 'Sample bio'
    assert remaining == ['bio']

def test_refs_expression_not_found():
    lookup_parts = ['nonexistent', 'path']
    annotations = {
        'username': User.objects.first().username,
        'username.profile': User.objects.first().profile,
    }
    result, remaining = refs_expression(lookup_parts, annotations)
    assert result is False
    assert remaining == ()

def test_refs_expression_partial_match():
    lookup_parts = ['username', 'profile', 'bio']
    annotations = {
        'username': User.objects.first().username,
        'username.profile': User.objects.first().profile,
    }
    result, remaining = refs_expression(lookup_parts, annotations)
    assert result == User.objects.first().profile
    assert remaining == ['bio']

def test_refs_expression_empty_lookup_parts():
    lookup_parts = []
    annotations = {
        'username': User.objects.first().username
    }
    result, remaining = refs_expression(lookup_parts, annotations)
    assert result is False
    assert remaining == ()

def test_refs_expression_no_annotations():
    lookup_parts = ['username', 'profile']
    annotations = {}
    result, remaining = refs_expression(lookup_parts, annotations)
    assert result is False
    assert remaining == ()