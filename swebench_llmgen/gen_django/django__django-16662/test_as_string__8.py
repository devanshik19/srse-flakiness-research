import pytest
from django.db import migrations
from django.contrib.auth.models import User
from django.utils.timezone import now

class DummyOperation:
    def __init__(self, name):
        self.name = name

class OperationWriter:
    def __init__(self, operation):
        self.operation = operation
    
    def serialize(self):
        return (f"migrations.RunPython(name={self.operation.name})", {self.operation.name})

@pytest.fixture
def migration():
    class MigrationStub:
        def __init__(self):
            self.operations = [DummyOperation('create_user'), DummyOperation('update_user')]
            self.dependencies = []
            self.replaces = None
            self.initial = False

    return MigrationStub()

def test_as_string_with_operations_and_dependencies(migration):
    writer = MigrationWriter(migration, include_header=True)
    
    result = writer.as_string()
    
    assert "migrations.RunPython(name=create_user)" in result
    assert "migrations.RunPython(name=update_user)" in result
    assert "from django.conf import settings" not in result  # No settings dependency
    assert "    replaces = None" not in result  # No replaces
    assert "initial = True" not in result  # Not initial
    assert "version" in result  # Check for version in header
    assert "timestamp" in result  # Check for timestamp in header

def test_as_string_with_replaces(migration):
    class MigrationWithReplaces:
        def __init__(self):
            self.operations = []
            self.dependencies = []
            self.replaces = ['001_initial']
            self.initial = False

    migration.replaces = ['001_initial']
    
    writer = MigrationWriter(migration, include_header=False)
    
    result = writer.as_string()
    
    assert "replaces = ('001_initial')" in result  # Check if replaces is handled