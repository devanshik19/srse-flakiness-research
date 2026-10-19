import pytest
from django.contrib.auth.models import User
from django.db.models.constants import LOOKUP_SEP
from django.db.models.query_utils import refs_expression

def test_refs_expression_found():
    lookup_parts = ['user', 'profile']
    annotations = {
        'user': True,
        'user' + LOOKUP_SEP + 'profile': True
    }
    result, remaining = refs_expression(lookup_parts, annotations)
    
    assert result is True
    assert remaining == []

def test_refs_expression_found_with_prefix():
    lookup_parts = ['user', 'details', 'address']
    annotations = {
        'user': True,
        'user' + LOOKUP_SEP + 'details': True,
        'user' + LOOKUP_SEP + 'details' + LOOKUP_SEP + 'address': True
    }
    result, remaining = refs_expression(lookup_parts, annotations)
    
    assert result is True
    assert remaining == ['address']

def test_refs_expression_not_found():
    lookup_parts = ['user', 'profile']
    annotations = {
        'group': True,
        'team': False
    }
    result, remaining = refs_expression(lookup_parts, annotations)
    
    assert result is False
    assert remaining == ()

def test_refs_expression_empty_annotations():
    lookup_parts = ['user', 'profile']
    annotations = {}
    result, remaining = refs_expression(lookup_parts, annotations)
    
    assert result is False
    assert remaining == ()

def test_refs_expression_empty_lookup_parts():
    lookup_parts = []
    annotations = {
        'user': True
    }
    result, remaining = refs_expression(lookup_parts, annotations)
    
    assert result is False
    assert remaining == ()