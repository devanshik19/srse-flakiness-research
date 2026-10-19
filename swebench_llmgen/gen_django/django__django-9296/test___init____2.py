import collections.abc
import pytest
from django.core.paginator import Paginator
from django.contrib.auth.models import User

def test_paginator_init_valid():
    user_list = [User(username=f'user{i}') for i in range(10)]
    paginator = Paginator(user_list, 5)

    assert paginator.object_list == user_list
    assert paginator.per_page == 5
    assert paginator.orphans == 0
    assert paginator.allow_empty_first_page is True

def test_paginator_init_with_orphans():
    user_list = [User(username=f'user{i}') for i in range(10)]
    paginator = Paginator(user_list, 5, orphans=2)

    assert paginator.orphans == 2

def test_paginator_init_invalid_per_page():
    user_list = [User(username=f'user{i}') for i in range(10)]
    
    with pytest.raises(ValueError):
        Paginator(user_list, 'invalid_per_page')

def test_paginator_init_empty_list():
    paginator = Paginator([], 5)

    assert paginator.object_list == []
    assert paginator.per_page == 5
    assert paginator.allow_empty_first_page is True

def test_paginator_init_no_allow_empty_first_page():
    user_list = [User(username=f'user{i}') for i in range(10)]
    paginator = Paginator(user_list, 5, allow_empty_first_page=False)

    assert paginator.allow_empty_first_page is False