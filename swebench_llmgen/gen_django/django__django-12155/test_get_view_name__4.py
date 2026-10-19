import pytest
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views import View
from django.apps import apps

# Focal function to be tested
def get_view_name(view_func):
    mod_name = view_func.__module__
    view_name = getattr(view_func, '__qualname__', view_func.__class__.__name__)
    return mod_name + '.' + view_name

# Sample view functions for testing
def sample_view(request):
    return HttpResponse("This is a sample view.")

class SampleClassView(View):
    def get(self, request):
        return HttpResponse("This is a class-based sample view.")

# Test cases
def test_get_view_name_function_based_view():
    view_name = get_view_name(sample_view)
    assert view_name == 'tests.test_get_view_name.sample_view'

def test_get_view_name_class_based_view():
    view_name = get_view_name(SampleClassView.as_view())
    assert view_name == 'tests.test_get_view_name.SampleClassView.get'