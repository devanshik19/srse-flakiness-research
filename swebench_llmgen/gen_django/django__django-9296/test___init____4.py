import pytest
from django.core.paginator import Paginator

def test_paginator_initialization():
    # Test with an empty object list
    paginator = Paginator([], per_page=10)
    assert paginator.object_list == []
    assert paginator.per_page == 10
    assert paginator.orphans == 0
    assert paginator.allow_empty_first_page is True

    # Test with a non-empty object list
    object_list = [1, 2, 3, 4, 5]
    paginator = Paginator(object_list, per_page=2)
    assert paginator.object_list == object_list
    assert paginator.per_page == 2
    assert paginator.orphans == 0
    assert paginator.allow_empty_first_page is True

    # Test with custom orphans and allow_empty_first_page
    paginator = Paginator(object_list, per_page=2, orphans=1, allow_empty_first_page=False)
    assert paginator.orphans == 1
    assert paginator.allow_empty_first_page is False

    # Test with non-integer per_page and orphans values
    paginator = Paginator(object_list, per_page='3', orphans='2')
    assert paginator.per_page == 3
    assert paginator.orphans == 2