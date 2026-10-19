import pytest
from django.core.paginator import Paginator
from django.contrib.auth.models import User

def test_paginator_init_with_valid_data():
    user_list = User.objects.all()[:10]  # Fetch 10 User objects from the database
    paginator = Paginator(user_list, per_page=2)

    assert paginator.object_list == user_list
    assert paginator.per_page == 2
    assert paginator.orphans == 0
    assert paginator.allow_empty_first_page is True

def test_paginator_init_with_orphans():
    user_list = User.objects.all()[:10]
    paginator = Paginator(user_list, per_page=2, orphans=1)

    assert paginator.orphans == 1

def test_paginator_init_with_empty_list():
    paginator = Paginator([], per_page=2)

    assert paginator.object_list == []
    assert paginator.allow_empty_first_page is True

def test_paginator_init_with_invalid_per_page():
    user_list = User.objects.all()[:10]

    with pytest.raises(ValueError):
        Paginator(user_list, per_page='not_a_number')

def test_paginator_init_with_orphans_negative():
    user_list = User.objects.all()[:10]

    with pytest.raises(ValueError):
        Paginator(user_list, per_page=2, orphans=-1)