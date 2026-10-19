import pytest
from django.contrib.auth.models import User
from django.db.models.constants import LOOKUP_SEP
from django.db.models.query_utils import refs_expression

def test_refs_expression_match():
    annotations = {
        'user__username': 'username_annotation',
        'user': 'user_annotation'
    }
    lookup_parts = ['user', 'username']
    result = refs_expression(lookup_parts, annotations)
    assert result == ('user_annotation', ['username'])

def test_refs_expression_partial_match():
    annotations = {
        'user__username': 'username_annotation',
        'user': 'user_annotation'
    }
    lookup_parts = ['user']
    result = refs_expression(lookup_parts, annotations)
    assert result == ('user_annotation', [])

def test_refs_expression_no_match():
    annotations = {
        'user__username': 'username_annotation'
    }
    lookup_parts = ['profile']
    result = refs_expression(lookup_parts, annotations)
    assert result == (False, ())

def test_refs_expression_empty_annotations():
    annotations = {}
    lookup_parts = ['user', 'username']
    result = refs_expression(lookup_parts, annotations)
    assert result == (False, ())

def test_refs_expression_multiple_levels():
    annotations = {
        'user': 'user_annotation',
        'user__username': 'username_annotation',
        'user__email': 'email_annotation'
    }
    lookup_parts = ['user', 'username', 'profile']
    result = refs_expression(lookup_parts, annotations)
    assert result == ('user_annotation', ['username', 'profile'])