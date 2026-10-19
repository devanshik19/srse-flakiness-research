import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.http import Http404

@pytest.mark.parametrize("url, expected_redirect", [
    ("some-view", True),  # Expect a redirect because of APPEND_SLASH setting
    ("some-view/", False),  # Expect no redirect because the URL already ends with '/'
])
def test_catch_all_view(client, url, expected_redirect):
    settings.APPEND_SLASH = True  # Set the APPEND_SLASH setting for tests
    admin_site = AdminSite()

    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    if expected_redirect:
        response = admin_site.catch_all_view(client.get(url, follow=True), url)
        assert isinstance(response, HttpResponsePermanentRedirect)
        assert response.status_code == 301
        assert response["Location"] == f"{client.get(url).request.build_absolute_uri()}/"
    else:
        with pytest.raises(Http404):
            admin_site.catch_all_view(client.get(url, follow=True), url)