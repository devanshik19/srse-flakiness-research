import pytest
from django.core.paginator import Paginator
from django.contrib.auth.models import User

def test_paginator_init():
    # Test with valid parameters
    user_list = User.objects.all()[:10]  # Assume there are at least 10 users
    paginator = Paginator(user_list, per_page=5)
    assert paginator.object_list == user_list
    assert paginator.per_page == 5
    assert paginator.orphans == 0
    assert paginator.allow_empty_first_page is True
    
    # Test with orphans
    paginator = Paginator(user_list, per_page=3, orphans=2)
    assert paginator.orphans == 2
    
    # Test with allow_empty_first_page set to False
    paginator = Paginator(user_list, per_page=5, allow_empty_first_page=False)
    assert paginator.allow_empty_first_page is False
    
    # Test for errors when passing non-integer values to per_page and orphans
    with pytest.raises(ValueError):
        Paginator(user_list, per_page='five')
    
    with pytest.raises(ValueError):
        Paginator(user_list, per_page=5, orphans='two')

    # Check ordering (adding minimal implementation for _check_object_list_is_ordered)
    with pytest.raises(Exception):
        Paginator(sorted(user_list, key=lambda x: x.username, reverse=True), per_page=2)