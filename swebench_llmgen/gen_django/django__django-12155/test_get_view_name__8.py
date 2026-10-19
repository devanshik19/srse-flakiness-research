import pytest
from django.contrib.auth.models import User
from django.http import HttpResponse


def dummy_view(request):
    return HttpResponse("Dummy View")


def test_get_view_name():
    # Test with a simple view function
    view_name = get_view_name(dummy_view)
    expected_name = f'{dummy_view.__module__}.dummy_view'
    assert view_name == expected_name

    # Test with a class-based view
    class DummyClassBasedView:
        def get(self, request):
            return HttpResponse("Class-Based Dummy View")

    view_name = get_view_name(DummyClassBasedView.get)
    expected_name = f'{DummyClassBasedView.__module__}.DummyClassBasedView.get'
    assert view_name == expected_name

    # Test with a method in a Django model
    user = User(username='testuser')
    view_name = get_view_name(user.save)
    expected_name = f'{User.__module__}.User.save'
    assert view_name == expected_name