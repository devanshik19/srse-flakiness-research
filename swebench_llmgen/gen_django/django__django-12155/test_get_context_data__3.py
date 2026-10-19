import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import RequestFactory
from django.views.generic import TemplateView

class BaseAdminDocsView(TemplateView):
    def get_context_data(self, **kwargs):
        return super().get_context_data(**{
            **kwargs,
            **admin.site.each_context(self.request),
        })

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def base_admin_docs_view(request_factory, user):
    request = request_factory.get('/')
    request.user = user
    return BaseAdminDocsView.as_view()(request)

def test_get_context_data_with_user(request_factory, user):
    request = request_factory.get('/')
    request.user = user
    view = BaseAdminDocsView.as_view()(request)
    context = view.get_context_data()
    assert 'admin' in context
    assert context['admin'] == site.each_context(request)

def test_get_context_data_without_user(request_factory):
    request = request_factory.get('/')
    view = BaseAdminDocsView.as_view()(request)
    context = view.get_context_data()
    assert 'admin' in context
    assert context['admin'] == site.each_context(request)

def test_get_context_data_with_extra_kwargs(request_factory, user):
    request = request_factory.get('/')
    request.user = user
    view = BaseAdminDocsView.as_view()(request)
    context = view.get_context_data(extra_key='extra_value')
    assert 'extra_key' in context
    assert context['extra_key'] == 'extra_value'
    assert 'admin' in context
    assert context['admin'] == site.each_context(request)