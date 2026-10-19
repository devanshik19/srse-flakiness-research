import pytest
from django.urls import reverse as django_reverse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import NoReverseMatch

# Ensure that a valid view function exists to reverse to
def sample_view(request):
    return HttpResponse("Sample View")

@pytest.mark.django_db
def test_reverse_without_arguments():
    # Test reversing with just the view name
    user = User.objects.create_user(username='testuser', password='testpassword')
    url = django_reverse('sample_view')
    assert url == "/sample_view/"

@pytest.mark.django_db
def test_reverse_with_namespace():
    # Test reversing with an app namespace
    user = User.objects.create_user(username='testuser', password='testpassword')
    
    # You would typically register your view with a namespace in a real app
    # To simulate this, we must ensure the resolver knows about our dummy view
    from django.urls import path, include
    from django.urls import reverse

    urlpatterns = [
        path('sample_view/', sample_view, name='sample_view'),
    ]
    
    # Attempt the reverse using the namespace
    url = reverse('app_name:sample_view')  # assuming 'app_name' is the namespace
    assert url == "/sample_view/"

@pytest.mark.django_db
def test_reverse_with_args():
    # Test reversing with arguments
    user = User.objects.create_user(username='testuser', password='testpassword')

    # Create a URL pattern that takes arguments
    urlpatterns = [
        path('user/<int:id>/', sample_view, name='user_view'),
    ]

    url = django_reverse('user_view', args=[user.id])
    assert url == f"/user/{user.id}/"

@pytest.mark.django_db
def test_reverse_with_kwargs():
    # Test reversing with keyword arguments
    user = User.objects.create_user(username='testuser', password='testpassword')

    # Create URL with keyword arguments
    urlpatterns = [
        path('user/<int:id>/', sample_view, name='user_view'),
    ]

    url = django_reverse('user_view', kwargs={'id': user.id})
    assert url == f"/user/{user.id}/"

@pytest.mark.django_db
def test_reverse_invalid_view_name():
    # Test reversing with an invalid view name
    with pytest.raises(NoReverseMatch):
        django_reverse('non_existent_view')