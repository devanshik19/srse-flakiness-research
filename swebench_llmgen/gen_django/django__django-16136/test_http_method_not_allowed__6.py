import pytest
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic.base import View

class TestView(View):
    http_method_names = ['get', 'post']

@pytest.fixture
def test_view():
    return TestView.as_view()

def test_http_method_not_allowed(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    response = test_view()(client.request('PUT', reverse('some-view-name')))
    
    assert isinstance(response, HttpResponseNotAllowed)
    assert response.status_code == 405
    assert response['Allow'] == 'GET, POST'