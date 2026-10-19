import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import CreateModel

@pytest.fixture
def create_model_instance():
    return CreateModel(name='User', fields=[], options={'proxy': False}, bases=[], managers=[])

def test_describe(create_model_instance):
    assert create_model_instance.describe() == "Create model User"

def test_describe_with_proxy(create_model_instance):
    create_model_instance.options['proxy'] = True
    assert create_model_instance.describe() == "Create proxy model User"