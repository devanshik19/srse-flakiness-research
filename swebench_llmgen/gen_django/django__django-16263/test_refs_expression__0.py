import pytest
from django.contrib.auth.models import User
from django.db.models.constants import LOOKUP_SEP
from django.db.models.query_utils import refs_expression

def test_refs_expression_found():
    annotations = {
        'name': 'Annotation for name',
        'email': 'Annotation for email',
        'profile__bio': 'Annotation for profile bio',
    }
    lookup_parts = ['profile', 'bio']
    result, remaining = refs_expression(lookup_parts, annotations)
    
    assert result == 'Annotation for profile bio'
    assert remaining == []

def test_refs_expression_partial_match():
    annotations = {
        'name': 'Annotation for name',
        'email': 'Annotation for email',
        'profile__bio': 'Annotation for profile bio',
    }
    lookup_parts = ['profile']
    result, remaining = refs_expression(lookup_parts, annotations)

    assert result == 'Annotation for profile bio'
    assert remaining == ['bio']

def test_refs_expression_not_found():
    annotations = {
        'name': 'Annotation for name',
        'email': 'Annotation for email',
    }
    lookup_parts = ['profile', 'bio']
    result, remaining = refs_expression(lookup_parts, annotations)

    assert result is False
    assert remaining == ()

def test_refs_expression_empty_lookup_parts():
    annotations = {
        'name': 'Annotation for name',
        'email': 'Annotation for email',
    }
    lookup_parts = []
    result, remaining = refs_expression(lookup_parts, annotations)

    assert result is False
    assert remaining == ()

def test_refs_expression_empty_annotations():
    annotations = {}
    lookup_parts = ['profile', 'bio']
    result, remaining = refs_expression(lookup_parts, annotations)

    assert result is False
    assert remaining == ()