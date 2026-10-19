import pytest
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.auth.models import User
from django.db import models

class TestModel(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()

class TestModelAdmin(BaseModelAdmin):
    model = TestModel

    def get_ordering(self, request):
        return ['username']

@pytest.fixture
def test_model_admin():
    return TestModelAdmin()

@pytest.fixture
def create_test_data():
    User.objects.create_user(username='testuser1', email='test1@example.com')
    User.objects.create_user(username='testuser2', email='test2@example.com')

def test_get_queryset_orders_correctly(test_model_admin, create_test_data):
    queryset = test_model_admin.get_queryset(None)
    assert queryset[0].username == 'testuser1'
    assert queryset[1].username == 'testuser2'