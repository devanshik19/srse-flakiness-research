import pytest
from django.urls import path
from django.contrib.auth.models import User
from django.http import HttpResponse

# The focal function to be tested
def get_view_name(view_func):
    mod_name = view_func.__module__
    view_name = getattr(view_func, '__qualname__', view_func.__class__.__name__)
    return mod_name + '.' + view_name

# Sample view function for testing
def sample_view(request):
    return HttpResponse("Sample View")

# Testing the get_view_name function
def test_get_view_name():
    # Test with a standard function
    assert get_view_name(sample_view) == 'path.to.module.sample_view'

    # Test with a class-based view (CBV)
    class SampleView:
        def get(self, request):
            return HttpResponse("Sample CBV Get")

    view_instance = SampleView()
    assert get_view_name(view_instance.get) == 'path.to.module.SampleView.get'

    # Test with a user created via the User model
    user_view = User.as_view()
    assert get_view_name(user_view) == 'django.contrib.auth.models.User.as_view'

    # Test with a callable attribute
    class AnotherSampleView:
        def some_method(self):
            return HttpResponse("Another Sample Method")

    another_view_instance = AnotherSampleView()
    assert get_view_name(another_view_instance.some_method) == 'path.to.module.AnotherSampleView.some_method'