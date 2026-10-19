import pytest
from django.db.backends.sqlite3.features import DatabaseFeatures
from django.contrib.auth.models import User

def test_django_test_skips():
    database_features = DatabaseFeatures()
    
    # Check expected skips for general version of SQLite
    skips = database_features.django_test_skips()
    assert 'SQLite stores values rounded to 15 significant digits.' in skips
    assert 'SQLite naively remakes the table on field alteration.' in skips
    assert "SQLite doesn't have a constraint." in skips
    assert "SQLite doesn't support negative precision for ROUND()." in skips
    
    # Check specific tests tied to the SQLite version
    if Database.sqlite_version_info < (3, 27):
        assert 'Nondeterministic failure on SQLite < 3.27.' in skips
    
    # Check for in-memory database specifics
    if database_features.connection.is_in_memory_db():
        assert "the sqlite backend's close() method is a no-op when using an in-memory database" in skips

    # Test the values for each skip
    assert skips['SQLite stores values rounded to 15 significant digits.'] == {
        'model_fields.test_decimalfield.DecimalFieldTests.test_fetch_from_db_without_float_rounding',
    }
    
    assert skips['SQLite naively remakes the table on field alteration.'] == {
        'schema.tests.SchemaTests.test_unique_no_unnecessary_fk_drops',
        'schema.tests.SchemaTests.test_unique_and_reverse_m2m',
        'schema.tests.SchemaTests.test_alter_field_default_doesnt_perform_queries',
        'schema.tests.SchemaTests.test_rename_column_renames_deferred_sql_references',
    }
    
    assert skips["SQLite doesn't have a constraint."] == {
        'model_fields.test_integerfield.PositiveIntegerFieldTests.test_negative_values',
    }
    
    assert skips["SQLite doesn't support negative precision for ROUND()."] == {
        'db_functions.math.test_round.RoundTests.test_null_with_negative_precision',
        'db_functions.math.test_round.RoundTests.test_decimal_with_negative_precision',
        'db_functions.math.test_round.RoundTests.test_float_with_negative_precision',
        'db_functions.math.test_round.RoundTests.test_integer_with_negative_precision',
    }

    if Database.sqlite_version_info < (3, 27):
        assert skips['Nondeterministic failure on SQLite < 3.27.'] == {
            'expressions_window.tests.WindowFunctionTests.test_subquery_row_range_rank',
        }

    if database_features.connection.is_in_memory_db():
        assert skips["the sqlite backend's close() method is a no-op when using an in-memory database"] == {
            'servers.test_liveserverthread.LiveServerThreadTest.test_closes_connections',
        }