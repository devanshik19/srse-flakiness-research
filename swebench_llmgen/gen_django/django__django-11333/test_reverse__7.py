import pytest
from django.urls import reverse as django_reverse
from django.urls.exceptions import NoReverseMatch
from django.contrib.auth.models import User
from django.urls import path

# Sample view function for testing
def sample_view(request):
    return HttpResponse("Sample view")

# URL patterns for the test
urlpatterns = [
    path('sample/', sample_view, name='sample_view'),
]

# Set up the test by overriding the default URLconf
@pytest.fixture(autouse=True)
def set_urlconf(settings):
    settings.ROOT_URLCONF = __name__

def test_reverse_with_valid_viewname():
    url = django_reverse('sample_view')
    assert url == '/sample/'

def test_reverse_with_namespaced_viewname():
    urlpatterns.append(path('namespace/sample/', sample_view, name='sample_view'))
    url = django_reverse('namespace:sample_view')
    assert url == '/namespace/sample/'

def test_reverse_with_no_namespace():
    url = django_reverse('sample_view')
    assert url == '/sample/'

def test_reverse_with_invalid_viewname():
    with pytest.raises(NoReverseMatch):
        django_reverse('non_existent_view')

def test_reverse_with_current_app():
    urlpatterns.append(path('app/sample/', sample_view, name='sample_view'))
    url = django_reverse('sample_view', current_app='app')
    assert url == '/app/sample/'

def test_reverse_with_extra_args():
    url = django_reverse('sample_view')
    assert url == '/sample/'  # No extra args needed but testing if it still works