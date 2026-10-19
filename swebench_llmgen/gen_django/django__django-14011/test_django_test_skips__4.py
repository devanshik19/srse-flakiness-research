import pytest
from django.db.backends.sqlite3.features import DatabaseFeatures
from django.contrib.auth.models import User

def test_django_test_skips():
    features = DatabaseFeatures()

    skips = features.django_test_skips()

    # Check the presence of known skips
    assert 'SQLite stores values rounded to 15 significant digits.' in skips
    assert 'model_fields.test_decimalfield.DecimalFieldTests.test_fetch_from_db_without_float_rounding' in skips['SQLite stores values rounded to 15 significant digits.']

    assert 'SQLite naively remakes the table on field alteration.' in skips
    assert 'schema.tests.SchemaTests.test_unique_no_unnecessary_fk_drops' in skips['SQLite naively remakes the table on field alteration.']

    assert "SQLite doesn't have a constraint." in skips
    assert 'model_fields.test_integerfield.PositiveIntegerFieldTests.test_negative_values' in skips["SQLite doesn't have a constraint."]

    assert "SQLite doesn't support negative precision for ROUND()." in skips
    assert 'db_functions.math.test_round.RoundTests.test_null_with_negative_precision' in skips["SQLite doesn't support negative precision for ROUND()."]

    # Simulate SQLite version < 3.27
    original_version_info = Database.sqlite_version_info
    Database.sqlite_version_info = (3, 26)  # Set to a version less than 3.27
    skips = features.django_test_skips()
    assert 'Nondeterministic failure on SQLite < 3.27.' in skips
    assert 'expressions_window.tests.WindowFunctionTests.test_subquery_row_range_rank' in skips['Nondeterministic failure on SQLite < 3.27.']
    Database.sqlite_version_info = original_version_info  # Reset to the original version

    # Simulate in-memory database
    conn_mock = features.connection
    original_is_in_memory_db = conn_mock.is_in_memory_db
    conn_mock.is_in_memory_db = lambda: True  # Simulate an in-memory DB
    skips = features.django_test_skips()
    assert "the sqlite backend's close() method is a no-op when using an in-memory database" in skips
    assert 'servers.test_liveserverthread.LiveServerThreadTest.test_closes_connections' in skips["the sqlite backend's close() method is a no-op when using an in-memory database"]
    conn_mock.is_in_memory_db = original_is_in_memory_db  # Reset to the original state