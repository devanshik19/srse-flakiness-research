import pytest
from django.core.paginator import Paginator
from django.contrib.auth.models import User

def test_paginator_init():
    # Test 1: Test basic initialization
    user_list = [User(username=f'user{i}') for i in range(5)]
    paginator = Paginator(user_list, per_page=2)
    
    assert paginator.object_list == user_list
    assert paginator.per_page == 2
    assert paginator.orphans == 0
    assert paginator.allow_empty_first_page is True

    # Test 2: Check orphans and empty first page
    paginator_with_orphans = Paginator(user_list, per_page=2, orphans=1, allow_empty_first_page=False)
    
    assert paginator_with_orphans.orphans == 1
    assert paginator_with_orphans.allow_empty_first_page is False

    # Test 3: Ensure ValueError is raised for invalid per_page
    with pytest.raises(ValueError):
        Paginator(user_list, per_page='invalid')

    # Test 4: Check empty object_list
    empty_paginator = Paginator([], per_page=2)
    assert empty_paginator.object_list == []
    assert empty_paginator.per_page == 2
    assert empty_paginator.allow_empty_first_page is True