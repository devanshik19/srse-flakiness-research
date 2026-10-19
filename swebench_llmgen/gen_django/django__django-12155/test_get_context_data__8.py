import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.views.generic import TemplateView
from django.urls import reverse
from .views import BaseAdminDocsView

class TestBaseAdminDocsView(BaseAdminDocsView):

    def dispatch(self, request):
        self.request = request
        return super().dispatch(request)

@pytest.mark.django_db
def test_get_context_data():
    user = User.objects.create_user(username='testuser', password='testpassword')
    request = HttpRequest()
    request.user = user

    # Create an instance of the test view
    view = TestBaseAdminDocsView.as_view()(request=request)

    # Call the method to be tested
    context = view.get_context_data(key='value')

    # Check the context returned by get_context_data
    assert context['key'] == 'value'
    assert context['site'] == site.each_context(request)['site']  # Check that admin context is included