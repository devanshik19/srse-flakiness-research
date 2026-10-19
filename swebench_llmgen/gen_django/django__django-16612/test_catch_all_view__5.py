import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.http import Http404
from django.urls import Resolver404, resolve
from django.conf import settings

@pytest.fixture
def admin_site():
    return AdminSite()

@pytest.mark.parametrize("url, expected_redirect", [
    ("http://testserver/someurl", "http://testserver/someurl/"),
    ("http://testserver/someurl/", None),
])
def test_catch_all_view(app, admin_site, url, expected_redirect):
    request = app.test_client().get(url)
    if expected_redirect:
        response = admin_site.catch_all_view(request, url)
        assert response.status_code == 301
        assert response["Location"] == expected_redirect
    else:
        with pytest.raises(Http404):
            admin_site.catch_all_view(request, url)

def test_catch_all_view_resolver404(admin_site):
    request = admin_site.get("http://testserver/nonexistent-url/")
    with pytest.raises(Http404):
        admin_site.catch_all_view(request, "http://testserver/nonexistent-url/")