import pytest
from django.core.paginator import Paginator
from django.contrib.auth.models import User

def test_paginator_init_valid_inputs():
    # Test with a valid object list and per_page
    user_list = [User(username=f'user{i}') for i in range(10)]
    paginator = Paginator(user_list, per_page=3)

    assert paginator.object_list == user_list
    assert paginator.per_page == 3
    assert paginator.orphans == 0
    assert paginator.allow_empty_first_page is True

def test_paginator_init_with_orphans():
    # Test with orphans parameter
    user_list = [User(username=f'user{i}') for i in range(10)]
    paginator = Paginator(user_list, per_page=3, orphans=2)

    assert paginator.orphans == 2

def test_paginator_init_empty_object_list():
    # Test with an empty object list
    paginator = Paginator([], per_page=5)

    assert paginator.object_list == []
    assert paginator.per_page == 5
    assert paginator.allow_empty_first_page is True

def test_paginator_init_non_empty_first_page():
    # Test with allow_empty_first_page set to False with a populated object list
    user_list = [User(username=f'user{i}') for i in range(5)]
    paginator = Paginator(user_list, per_page=3, allow_empty_first_page=False)

    assert paginator.allow_empty_first_page is False

def test_paginator_init_invalid_per_page():
    # Test with an invalid per_page value
    user_list = [User(username=f'user{i}') for i in range(10)]
    
    with pytest.raises(ValueError):
        Paginator(user_list, per_page='invalid')

def test_paginator_init_orphans_as_string():
    # Test with orphans as a string, which should raise an error
    user_list = [User(username=f'user{i}') for i in range(10)]
    
    with pytest.raises(ValueError):
        Paginator(user_list, per_page=3, orphans='invalid')