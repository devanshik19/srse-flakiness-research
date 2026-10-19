import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query_instance():
    user = User.objects.create(username='testuser', password='testpass')
    return Query(model=User, where=None)

def test_clear_select_fields(query_instance):
    # Set some select fields
    query_instance.select = ('id', 'username')
    query_instance.values_select = ('username',)

    # Verify fields are set
    assert query_instance.select == ('id', 'username')
    assert query_instance.values_select == ('username',)

    # Clear fields
    query_instance.clear_select_fields()

    # Verify fields are cleared
    assert query_instance.select == ()
    assert query_instance.values_select == ()