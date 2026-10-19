import pytest
from django.urls import reverse as django_reverse
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.urls import NoReverseMatch

# Sample view for testing
from django.http import HttpResponse
from django.urls import path

def sample_view(request):
    return HttpResponse("Sample view")

urlpatterns = [
    path('sample/', sample_view, name='sample_view'),
]

def test_reverse_without_namespace():
    url = django_reverse('sample_view')
    assert url == '/sample/'

def test_reverse_with_arguments():
    url = django_reverse('sample_view')
    assert url == '/sample/'

def test_reverse_with_unknown_view():
    with pytest.raises(NoReverseMatch):
        django_reverse('unknown_view')

def test_reverse_with_namespace():
    # Creating a namespace
    urlpatterns_ns = [
        path('app/sample/', sample_view, name='sample_view')
    ]

    # Register the URL configuration with a namespace
    from django.urls import include
    urlpatterns = [
        path('app/', include((urlpatterns_ns, 'app_namespace'), namespace='app_namespace'))
    ]
    
    url = django_reverse('app_namespace:sample_view')
    assert url == '/app/sample/'

def test_reverse_with_invalid_namespace():
    with pytest.raises(NoReverseMatch):
        django_reverse('invalid_namespace:sample_view')