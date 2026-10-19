import pytest
from django.contrib.auth.models import User
from django.urls import path

# Assuming the function is imported directly from the module
from django.contrib.admindocs.utils import get_view_name

def sample_view(request):
    pass

urlpatterns = [
    path('sample/', sample_view, name='sample_view'),
]

def test_get_view_name():
    view_func = sample_view
    expected_view_name = f"{view_func.__module__}.{view_func.__qualname__}"
    
    assert get_view_name(view_func) == expected_view_name

    # Test with a class-based view
    class SampleView:
        def get(self, request):
            pass

    view_func_class = SampleView.get
    expected_view_name_class = f"{SampleView.__module__}.{SampleView.__qualname__}"
    
    assert get_view_name(view_func_class) == expected_view_name_class