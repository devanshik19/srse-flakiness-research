import pytest
from django.contrib.auth.models import User
from django.urls import path
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admindocs.utils import get_view_name

# Sample view functions for testing
def simple_view(request):
    return HttpResponse("Hello, World!")

@method_decorator(csrf_exempt, name='dispatch')
class SampleView(View):
    def get(self, request):
        return HttpResponse("Sample View")

# Create test cases
def test_get_view_name_for_function_view():
    view_name = get_view_name(simple_view)
    assert view_name == 'django.contrib.admindocs.utils.simple_view'

def test_get_view_name_for_class_based_view():
    view_name = get_view_name(SampleView.as_view())
    assert view_name == 'django.contrib.admindocs.utils.SampleView.get'