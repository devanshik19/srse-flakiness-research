import pytest
from django.db.backends.sqlite3.features import DatabaseFeatures
from django.contrib.auth.models import User

def test_django_test_skips():
    db_features = DatabaseFeatures()

    # Retrieve the skips dictionary
    skips = db_features.django_test_skips()

    # Check specific keys in the skips dictionary
    assert 'SQLite stores values rounded to 15 significant digits.' in skips
    assert 'model_fields.test_decimalfield.DecimalFieldTests.test_fetch_from_db_without_float_rounding' in skips['SQLite stores values rounded to 15 significant digits.']

    assert 'SQLite naively remakes the table on field alteration.' in skips
    assert 'schema.tests.SchemaTests.test_unique_no_unnecessary_fk_drops' in skips['SQLite naively remakes the table on field alteration.']

    assert "SQLite doesn't have a constraint." in skips
    assert 'model_fields.test_integerfield.PositiveIntegerFieldTests.test_negative_values' in skips["SQLite doesn't have a constraint."]

    assert "SQLite doesn't support negative precision for ROUND()." in skips
    assert 'db_functions.math.test_round.RoundTests.test_null_with_negative_precision' in skips["SQLite doesn't support negative precision for ROUND()."]

    # Check for version-specific skips
    if Database.sqlite_version_info < (3, 27):
        assert 'Nondeterministic failure on SQLite < 3.27.' in skips
        assert 'expressions_window.tests.WindowFunctionTests.test_subquery_row_range_rank' in skips['Nondeterministic failure on SQLite < 3.27.']

    # Check for in-memory database skips
    if db_features.connection.is_in_memory_db():
        assert "the sqlite backend's close() method is a no-op when using an in-memory database" in skips
        assert 'servers.test_liveserverthread.LiveServerThreadTest.test_closes_connections' in skips["the sqlite backend's close() method is a no-op when using an in-memory database"]