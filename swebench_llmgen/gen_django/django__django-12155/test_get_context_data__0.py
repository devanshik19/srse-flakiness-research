import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.views import View

class BaseAdminDocsView(View):
    def get_context_data(self, **kwargs):
        return super().get_context_data(**{
            **kwargs,
            **admin.site.each_context(self.request),
        })

@pytest.fixture
def base_admin_docs_view():
    return BaseAdminDocsView.as_view()

def test_get_context_data(base_admin_docs_view):
    request = HttpRequest()
    request.user = User(username='testuser')
    request.user.is_staff = True
    request.user.is_active = True
    request.META['HTTP_HOST'] = 'testserver'

    # Simulate request to context data
    response = base_admin_docs_view(request)

    # Ensure the response is a TemplateResponse
    assert isinstance(response, TemplateResponse)

    # Check if the context contains admin site info
    context = response.context_data
    assert 'admin' in context
    assert context['admin'] == site

    # Check for additional context if any kwargs are passed
    custom_context_data = {'foo': 'bar'}
    response_with_kwargs = base_admin_docs_view(request, **custom_context_data)
    context_with_kwargs = response_with_kwargs.context_data

    assert context_with_kwargs['foo'] == 'bar'
    assert context_with_kwargs['admin'] == site

    # Ensure the request is set correctly
    assert context['request'] == request