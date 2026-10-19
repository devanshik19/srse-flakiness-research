import pytest
from django.core.paginator import Paginator
from django.contrib.auth.models import User

def test_paginator_init_valid_args():
    # Create a list of user instances for the object_list
    users = [User(username=f'user{i}') for i in range(10)]
    
    # Test Paginator with valid parameters
    paginator = Paginator(object_list=users, per_page=5, orphans=1, allow_empty_first_page=True)
    
    assert paginator.object_list == users
    assert paginator.per_page == 5
    assert paginator.orphans == 1
    assert paginator.allow_empty_first_page is True

def test_paginator_init_invalid_per_page():
    users = [User(username=f'user{i}') for i in range(10)]
    
    # Test Paginator with invalid per_page (string)
    with pytest.raises(ValueError):
        Paginator(object_list=users, per_page='five')

def test_paginator_init_invalid_orphans():
    users = [User(username=f'user{i}') for i in range(10)]
    
    # Test Paginator with invalid orphans (negative integer)
    with pytest.raises(ValueError):
        Paginator(object_list=users, per_page=5, orphans=-1)

def test_paginator_init_empty_object_list():
    # Test Paginator with an empty object list
    paginator = Paginator(object_list=[], per_page=5)
    
    assert paginator.object_list == []
    assert paginator.per_page == 5
    assert paginator.allow_empty_first_page is True