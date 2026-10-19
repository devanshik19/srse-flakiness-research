import pytest
from django.contrib.auth.models import User
from django.db.models.constants import LOOKUP_SEP
from django.db.models.query_utils import refs_expression

def test_refs_expression_found():
    lookup_parts = ['username']
    annotations = {
        'username': 'some_username_annotation',
        'email': 'email_annotation'
    }
    
    result_value, remaining_parts = refs_expression(lookup_parts, annotations)
    
    assert result_value == 'some_username_annotation'
    assert remaining_parts == []

def test_refs_expression_partial_found():
    lookup_parts = ['username', 'email']
    annotations = {
        'username': 'some_username_annotation',
        'username__exact': 'exact_username_annotation',
        'email': 'email_annotation'
    }

    result_value, remaining_parts = refs_expression(lookup_parts, annotations)

    assert result_value == 'some_username_annotation'
    assert remaining_parts == ['email']

def test_refs_expression_not_found():
    lookup_parts = ['age']
    annotations = {
        'username': 'some_username_annotation',
        'email': 'email_annotation'
    }

    result_value, remaining_parts = refs_expression(lookup_parts, annotations)

    assert result_value == False
    assert remaining_parts == ()

def test_refs_expression_multiple_parts_found():
    lookup_parts = ['username', 'email']
    annotations = {
        'username': 'some_username_annotation',
        'username__exact': 'exact_username_annotation',
        'email': 'email_annotation',
        'username__first_name': 'first_name_annotation'
    }

    result_value, remaining_parts = refs_expression(lookup_parts, annotations)

    assert result_value == 'some_username_annotation'
    assert remaining_parts == ['email']