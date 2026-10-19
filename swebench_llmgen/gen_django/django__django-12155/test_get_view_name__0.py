import pytest
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.admindocs.utils import get_view_name

def sample_view(request):
    return HttpResponse("Sample View")

urlpatterns = [
    path('sample/', sample_view, name='sample_view'),
]

def test_get_view_name():
    view_name = get_view_name(sample_view)
    expected_view_name = 'django.contrib.admindocs.utils.sample_view'
    assert view_name == expected_view_name

    user_view_name = get_view_name(User)
    expected_user_view_name = 'django.contrib.auth.models.User'
    assert user_view_name == expected_user_view_name

    class CustomView:
        def method(self):
            pass

    custom_view_name = get_view_name(CustomView.method)
    expected_custom_view_name = 'builtins.CustomView.method'
    assert custom_view_name == expected_custom_view_name