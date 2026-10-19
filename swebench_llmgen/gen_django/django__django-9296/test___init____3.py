import pytest
from django.core.paginator import Paginator
from django.contrib.auth.models import User

def test_paginator_init_with_valid_inputs():
    user_list = [User(username=f'user{i}') for i in range(10)]
    paginator = Paginator(user_list, per_page=3, orphans=2, allow_empty_first_page=True)

    assert paginator.object_list == user_list
    assert paginator.per_page == 3
    assert paginator.orphans == 2
    assert paginator.allow_empty_first_page is True

def test_paginator_init_with_empty_list():
    paginator = Paginator([], per_page=3, orphans=0, allow_empty_first_page=True)

    assert paginator.object_list == []
    assert paginator.per_page == 3
    assert paginator.orphans == 0
    assert paginator.allow_empty_first_page is True

def test_paginator_init_with_negative_per_page():
    with pytest.raises(ValueError):
        Paginator([User()], per_page=-1)

def test_paginator_init_with_non_integer_per_page():
    with pytest.raises(ValueError):
        Paginator([User()], per_page='two')

def test_paginator_init_with_non_integer_orphans():
    with pytest.raises(ValueError):
        Paginator([User()], orphans='two')

def test_paginator_init_with_non_boolean_allow_empty_first_page():
    with pytest.raises(ValueError):
        Paginator([User()], allow_empty_first_page='yes')