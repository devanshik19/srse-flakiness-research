import pytest
from django.core.paginator import Paginator
from django.contrib.auth.models import User

def test_paginator_init_valid_input():
    users = list(User.objects.all())  # Assuming there are some User instances in the test database.
    paginator = Paginator(users, 10, orphans=1, allow_empty_first_page=True)
    
    assert paginator.object_list == users
    assert paginator.per_page == 10
    assert paginator.orphans == 1
    assert paginator.allow_empty_first_page is True

def test_paginator_init_invalid_per_page():
    users = list(User.objects.all())
    with pytest.raises(ValueError):
        Paginator(users, 'ten')

def test_paginator_init_invalid_orphans():
    users = list(User.objects.all())
    with pytest.raises(ValueError):
        Paginator(users, 10, orphans='one')

def test_paginator_init_negative_per_page():
    users = list(User.objects.all())
    with pytest.raises(ValueError):
        Paginator(users, -5)

def test_paginator_init_empty_object_list():
    paginator = Paginator([], 10, orphans=0, allow_empty_first_page=True)
    
    assert paginator.object_list == []
    assert paginator.per_page == 10
    assert paginator.orphans == 0
    assert paginator.allow_empty_first_page is True