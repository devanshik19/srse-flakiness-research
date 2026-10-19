import pytest
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.views.generic.base import View

class TestView(View):
    http_method_names = ['get', 'post']

    def _allowed_methods(self):
        return self.http_method_names

    def http_method_not_allowed(self, request, *args, **kwargs):
        logger.warning(
            "Method Not Allowed (%s): %s",
            request.method,
            request.path,
            extra={"status_code": 405, "request": request},
        )
        return HttpResponseNotAllowed(self._allowed_methods())

@pytest.mark.django_db
def test_http_method_not_allowed(client):
    view = TestView.as_view()
    request_post = client.post(reverse('some-url-name'))  # Assuming a URL that allows only GET

    response = view(request_post)

    assert isinstance(response, HttpResponseNotAllowed)
    assert response.status_code == 405
    assert 'get' in response['Allow']  # Check allowed methods
    assert 'post' not in response['Allow']  # POST should not be allowed