import pytest
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.admindocs.utils import get_view_name

# Sample view function for testing
def sample_view(request):
    return HttpResponse("Sample View")

urlpatterns = [
    path('sample/', sample_view, name='sample'),
]

def test_get_view_name():
    # Test the view function
    expected_name = f"{sample_view.__module__}.sample_view"
    assert get_view_name(sample_view) == expected_name

    # Test the view function with qualified name
    class SampleClass:
        def method(self, request):
            return HttpResponse("Method View")
    
    expected_class_name = f"{SampleClass.__module__}.SampleClass.method"
    assert get_view_name(SampleClass.method) == expected_class_name

    # Ensure that a class method returns the correct qualified name
    obj = SampleClass()
    expected_instance_name = f"{obj.__module__}.SampleClass.method"
    assert get_view_name(obj.method) == expected_instance_name

    # Test view name without qualified name, should fall back to class name
    def another_sample_view(request):
        return HttpResponse("Another Sample View")
    
    another_expected_name = f"{another_sample_view.__module__}.another_sample_view"
    assert get_view_name(another_sample_view) == another_expected_name