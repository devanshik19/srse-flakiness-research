import pytest
from django.urls import reverse as django_reverse
from django.contrib.auth.models import User
from django.urls import path


# Sample view function for testing
def dummy_view(request):
    return "dummy response"


# Sample URL patterns for testing
urlpatterns = [
    path('dummy/', dummy_view, name='dummy_view'),
]

# Adding patterns to Django's URL resolver for test case
from django.urls import include
from django.conf import settings
from django.core.management import call_command


@pytest.fixture(autouse=True)
def setup_django_urls(settings):
    settings.ROOT_URLCONF = 'django.urls.base'  # Use the base module to import patterns
    settings.URLCONF = urlpatterns
    call_command('migrate')  # Ensure we have migrations run for tests


def test_reverse_with_valid_view_name():
    url = django_reverse('dummy_view')
    assert url == '/dummy/'


def test_reverse_with_invalid_view_name():
    with pytest.raises(NoReverseMatch):
        django_reverse('non_existing_view')


def test_reverse_with_namespaces():
    urlpatterns.append(path('namespace/', include((urlpatterns, 'namespace'))))
    
    url = django_reverse('namespace:dummy_view')
    assert url == '/namespace/dummy/'


def test_reverse_with_app_name_but_no_namespace():
    url = django_reverse('dummy_view', current_app='namespace')
    assert url == '/dummy/'


def test_reverse_with_args():
    urlpatterns.append(path('user/<int:id>/', dummy_view, name='user_detail'))
    url = django_reverse('user_detail', args=[1])
    assert url == '/user/1/'


def test_reverse_with_kwargs():
    url = django_reverse('user_detail', kwargs={'id': 1})
    assert url == '/user/1/'


def test_reverse_with_non_string_viewname():
    user = User.objects.create(username='testuser')
    url = django_reverse(dummy_view, kwargs={'id': user.id})
    assert url == '/dummy/'  # Ensure direct call gives the same result