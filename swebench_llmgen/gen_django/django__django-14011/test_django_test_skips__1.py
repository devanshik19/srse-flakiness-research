import pytest
from django.db.backends.sqlite3.features import DatabaseFeatures
from django.contrib.auth.models import User

def test_django_test_skips():
    db_features = DatabaseFeatures()

    skips = db_features.django_test_skips()
    
    assert 'SQLite stores values rounded to 15 significant digits.' in skips
    assert 'SQLite naively remakes the table on field alteration.' in skips
    assert "SQLite doesn't have a constraint." in skips
    assert "SQLite doesn't support negative precision for ROUND()." in skips

    assert 'model_fields.test_decimalfield.DecimalFieldTests.test_fetch_from_db_without_float_rounding' in skips['SQLite stores values rounded to 15 significant digits.']

    assert 'schema.tests.SchemaTests.test_unique_no_unnecessary_fk_drops' in skips['SQLite naively remakes the table on field alteration.']
    assert 'schema.tests.SchemaTests.test_unique_and_reverse_m2m' in skips['SQLite naively remakes the table on field alteration.']
    assert 'schema.tests.SchemaTests.test_alter_field_default_doesnt_perform_queries' in skips['SQLite naively remakes the table on field alteration.']
    assert 'schema.tests.SchemaTests.test_rename_column_renames_deferred_sql_references' in skips['SQLite naively remakes the table on field alteration.']

    assert 'model_fields.test_integerfield.PositiveIntegerFieldTests.test_negative_values' in skips["SQLite doesn't have a constraint."]

    assert 'db_functions.math.test_round.RoundTests.test_null_with_negative_precision' in skips["SQLite doesn't support negative precision for ROUND()."]
    assert 'db_functions.math.test_round.RoundTests.test_decimal_with_negative_precision' in skips["SQLite doesn't support negative precision for ROUND()."]
    assert 'db_functions.math.test_round.RoundTests.test_float_with_negative_precision' in skips["SQLite doesn't support negative precision for ROUND()."]
    assert 'db_functions.math.test_round.RoundTests.test_integer_with_negative_precision' in skips["SQLite doesn't support negative precision for ROUND()."]

    if Database.sqlite_version_info < (3, 27):
        assert 'Nondeterministic failure on SQLite < 3.27.' in skips

    if db_features.connection.is_in_memory_db():
        assert "the sqlite backend's close() method is a no-op when using an in-memory database" in skips