import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.operations.models import CreateModel

@pytest.fixture
def create_model_instance():
    return CreateModel(name='User', fields=[('username', models.CharField(max_length=150))], options={}, bases=None, managers=None)

def test_describe_standard(create_model_instance):
    result = create_model_instance.describe()
    assert result == "Create model User"

def test_describe_proxy(create_model_instance):
    create_model_instance.options['proxy'] = True
    result = create_model_instance.describe()
    assert result == "Create proxy model User"