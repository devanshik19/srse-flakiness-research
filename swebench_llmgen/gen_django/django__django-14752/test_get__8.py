import pytest
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.urls import reverse
from django.test import RequestFactory
from django.apps import apps
from django.contrib.admin import ModelAdmin


class AutocompleteJsonView(ModelAdmin):
    paginate_by = 10
    admin_site = None  # dummy for test

    def get(self, request, *args, **kwargs):
        self.term, self.model_admin, self.source_field, to_field_name = self.process_request(request)

        if not self.has_perm(request):
            raise PermissionDenied

        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {'id': str(getattr(obj, to_field_name)), 'text': str(obj)}
                for obj in context['object_list']
            ],
            'pagination': {'more': context['page_obj'].has_next()},
        })

    def process_request(self, request):
        # For the sake of testing, we assume these values are returned
        return ('term', self, 'source_field', 'id')

    def has_perm(self, request):
        return request.user.has_perm('auth.view_user')

    def get_queryset(self):
        return User.objects.all()[:self.paginate_by]

    def get_context_data(self):
        # Simplified for testing
        object_list = self.get_queryset()
        return {
            'object_list': object_list,
            'page_obj': self
        }


@pytest.mark.django_db
def test_autocomplete_json_view_get_permissions(client):
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_login(user)

    view = AutocompleteJsonView(admin_site=None)
    request = RequestFactory().get('/autocomplete/')
    request.user = user

    response = view.get(request)

    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    assert 'results' in response.json()
    assert len(response.json()['results']) <= view.paginate_by


@pytest.mark.django_db
def test_autocomplete_json_view_get_permission_denied(client):
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_login(user)

    view = AutocompleteJsonView(admin_site=None)

    def mock_has_perm(request):
        return False

    view.has_perm = mock_has_perm

    request = RequestFactory().get('/autocomplete/')
    request.user = user

    with pytest.raises(PermissionDenied):
        view.get(request)