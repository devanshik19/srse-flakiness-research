import pytest
from django.contrib.auth.models import User
from django.db.migrations.autodetector import MigrationAutodetector

@pytest.fixture
def migration_autodetector():
    return MigrationAutodetector(None, None, None)

def test_only_relation_agnostic_fields(migration_autodetector):
    # Create a model field with a ForeignKey
    user_field = User._meta.get_field('groups')

    # Create a dictionary of fields
    fields = {
        'user_field': user_field,
        'username': User._meta.get_field('username'),
        'email': User._meta.get_field('email')
    }
    
    # Expected result after calling only_relation_agnostic_fields
    # The ForeignKey 'user_field' deconstruction should not have 'to' in its definition
    expected_fields_def = [
        ('user_field', ('auth.User', 'groups', '', 'ForeignKey', {}, {'on_delete': 'CASCADE', 'related_name': 'user_field_related'})),
        ('username', ('auth.User', 'username', '', 'CharField', {'max_length': 150, 'unique': True}, {})),
        ('email', ('auth.User', 'email', '', 'EmailField', {'max_length': 254, 'blank': True, 'null': True}, {})),
    ]

    # Call the method to test
    actual_fields_def = migration_autodetector.only_relation_agnostic_fields(fields)

    # Compare the actual result to the expected result
    assert actual_fields_def == expected_fields_def