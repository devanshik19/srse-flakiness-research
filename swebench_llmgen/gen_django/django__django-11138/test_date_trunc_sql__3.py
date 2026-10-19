import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

class TestDatabaseOperations:
    def setup_method(self):
        self.db_ops = DatabaseOperations()

    def test_date_trunc_sql(self):
        # Test with various lookup types and field names
        result = self.db_ops.date_trunc_sql('second', 'created_at')
        assert result == "django_date_trunc('second', created_at)"

        result = self.db_ops.date_trunc_sql('HOUR', 'login_time')
        assert result == "django_date_trunc('hour', login_time)"

        result = self.db_ops.date_trunc_sql('DAY', 'birth_date')
        assert result == "django_date_trunc('day', birth_date)"

        result = self.db_ops.date_trunc_sql('MONTH', 'event_date')
        assert result == "django_date_trunc('month', event_date)"

        result = self.db_ops.date_trunc_sql('YEAR', 'registration_date')
        assert result == "django_date_trunc('year', registration_date)"