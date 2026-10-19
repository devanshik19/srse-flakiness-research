import pytest
from django.core.paginator import Paginator
from django.contrib.auth.models import User

def test_paginator_init_with_valid_data():
    users = [User(username=f'user{i}') for i in range(10)]
    paginator = Paginator(users, per_page=2)

    assert paginator.object_list == users
    assert paginator.per_page == 2
    assert paginator.orphans == 0
    assert paginator.allow_empty_first_page is True

def test_paginator_init_with_empty_list():
    paginator = Paginator([], per_page=2)

    assert paginator.object_list == []
    assert paginator.per_page == 2
    assert paginator.orphans == 0
    assert paginator.allow_empty_first_page is True

def test_paginator_init_with_orphans():
    users = [User(username=f'user{i}') for i in range(10)]
    paginator = Paginator(users, per_page=3, orphans=1)

    assert paginator.object_list == users
    assert paginator.per_page == 3
    assert paginator.orphans == 1
    assert paginator.allow_empty_first_page is True

def test_paginator_init_with_allow_empty_first_page_false():
    users = [User(username=f'user{i}') for i in range(10)]
    paginator = Paginator(users, per_page=3, allow_empty_first_page=False)

    assert paginator.object_list == users
    assert paginator.per_page == 3
    assert paginator.orphans == 0
    assert paginator.allow_empty_first_page is False

def test_paginator_init_with_non_integer_per_page():
    with pytest.raises(ValueError):
        Paginator([], per_page='two')