import pytest
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.admindocs.utils import get_view_name

# Sample view function for testing
def example_view(request):
    return HttpResponse("Example View")

def another_example_view(request):
    return HttpResponse("Another Example View")

urlpatterns = [
    path('example/', example_view, name='example_view'),
    path('another_example/', another_example_view, name='another_example_view'),
]

def test_get_view_name():
    # Test case for a straightforward function
    assert get_view_name(example_view) == 'django.contrib.admindocs.utils.example_view'
    
    # Test case for another function
    assert get_view_name(another_example_view) == 'django.contrib.admindocs.utils.another_example_view'
    
    # Check with a class-based view if covered
    class ExampleClassView:
        def dispatch(self, request):
            return HttpResponse("Class based view response")
    
    assert get_view_name(ExampleClassView.dispatch) == 'django.contrib.admindocs.utils.ExampleClassView.dispatch'