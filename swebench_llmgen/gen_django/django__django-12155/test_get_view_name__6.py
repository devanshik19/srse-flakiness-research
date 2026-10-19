import pytest
from django.http import HttpResponse

from django.contrib.admidocs.utils import get_view_name

def sample_view(request):
    return HttpResponse("Sample View")

def another_view():
    return HttpResponse("Another View")

def test_get_view_name_for_sample_view():
    assert get_view_name(sample_view) == 'django.contrib.admindocs.utils.sample_view'

def test_get_view_name_for_another_view():
    assert get_view_name(another_view) == 'django.contrib.admindocs.utils.another_view'

def test_get_view_name_for_class_based_view():
    class SampleClassBasedView:
        def get(self, request):
            return HttpResponse("Class Based View")

    view_instance = SampleClassBasedView()
    assert get_view_name(view_instance.get) == 'django.contrib.admindocs.utils.SampleClassBasedView.get'