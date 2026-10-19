import pytest
from django.http import HttpResponse

from django.contrib.admindocs.utils import get_view_name

def test_get_view_name_function():
    def sample_view(request):
        return HttpResponse("Sample View")

    # Test with a function view
    assert get_view_name(sample_view) == 'tests.test_get_view_name_function.sample_view'

def test_get_view_name_class_based_view():
    from django.views import View

    class SampleClassView(View):
        def get(self, request):
            return HttpResponse("Sample Class-based View")

    # Test with a class-based view
    assert get_view_name(SampleClassView.as_view()) == 'tests.test_get_view_name_function.SampleClassView.get'