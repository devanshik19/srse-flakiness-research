import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet

@pytest.mark.django_db
def test_set_values():
    # Create a user instance to use in the QuerySet
    user = User.objects.create_user(username='testuser', password='testpass')

    # Initialize a Query object with the User model
    query = user._default_manager.all().query

    # Test setting values with explicit fields
    fields = ['username', 'email']
    query.set_values(fields)
    assert query.values_select == ('username', 'email')

    # Test setting values with extra and annotations being empty
    fields = []
    query.set_values(fields)
    assert query.values_select == tuple(field.attname for field in User._meta.concrete_fields)

    # Test with extra_select fields
    query.extra_select = {'extra_field': 'extra_value'}
    fields = ['username', 'extra_field']
    query.set_values(fields)
    assert query.values_select == ('username', 'extra_field')

    # Test with annotation select
    query.annotation_select = {'bio': 'bio_annotation'}
    fields = ['username', 'bio']
    query.set_values(fields)
    assert query.values_select == ('username', 'bio')

    # Test with group_by set to True
    query.group_by = True
    query.set_values(['username'])
    assert query.values_select == ('username',)

    # Test with group_by set with multiple fields
    query.group_by = ['username', 'email']
    query.set_values(['username', 'email'])
    assert query.group_by == ('username', 'email')

    # Check that select_related is set to False after calling set_values
    assert not query.select_related
    # Ensure deferred loading is cleared
    query.add_deferred_loading(['last_login'])
    query.set_values(['username'])
    assert query.deferred_loading == []

    # Verify that extra masks are set correctly
    assert query.extra_select_mask == set()
    query.set_extra_mask(['extra_field'])
    assert query.extra_select_mask == {'extra_field'}
    
    # Check annotation masks
    assert query.annotation_select_mask == set()
    query.set_annotation_mask(['bio'])
    assert query.annotation_select_mask == {'bio'}