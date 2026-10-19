import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.features import DatabaseFeatures
from django.db import connection

@pytest.mark.parametrize("sqlite_version_info, in_memory_db, expected_skips", [
    ((3, 26), False, {
        'SQLite stores values rounded to 15 significant digits.': {
            'model_fields.test_decimalfield.DecimalFieldTests.test_fetch_from_db_without_float_rounding',
        },
        'SQLite naively remakes the table on field alteration.': {
            'schema.tests.SchemaTests.test_unique_no_unnecessary_fk_drops',
            'schema.tests.SchemaTests.test_unique_and_reverse_m2m',
            'schema.tests.SchemaTests.test_alter_field_default_doesnt_perform_queries',
            'schema.tests.SchemaTests.test_rename_column_renames_deferred_sql_references',
        },
        "SQLite doesn't have a constraint.": {
            'model_fields.test_integerfield.PositiveIntegerFieldTests.test_negative_values',
        },
        "SQLite doesn't support negative precision for ROUND().": {
            'db_functions.math.test_round.RoundTests.test_null_with_negative_precision',
            'db_functions.math.test_round.RoundTests.test_decimal_with_negative_precision',
            'db_functions.math.test_round.RoundTests.test_float_with_negative_precision',
            'db_functions.math.test_round.RoundTests.test_integer_with_negative_precision',
        },
    }),
    ((3, 27), False, {
        'SQLite stores values rounded to 15 significant digits.': {
            'model_fields.test_decimalfield.DecimalFieldTests.test_fetch_from_db_without_float_rounding',
        },
        'SQLite naively remakes the table on field alteration.': {
            'schema.tests.SchemaTests.test_unique_no_unnecessary_fk_drops',
            'schema.tests.SchemaTests.test_unique_and_reverse_m2m',
            'schema.tests.SchemaTests.test_alter_field_default_doesnt_perform_queries',
            'schema.tests.SchemaTests.test_rename_column_renames_deferred_sql_references',
        },
        "SQLite doesn't have a constraint.": {
            'model_fields.test_integerfield.PositiveIntegerFieldTests.test_negative_values',
        },
        "SQLite doesn't support negative precision for ROUND().": {
            'db_functions.math.test_round.RoundTests.test_null_with_negative_precision',
            'db_functions.math.test_round.RoundTests.test_decimal_with_negative_precision',
            'db_functions.math.test_round.RoundTests.test_float_with_negative_precision',
            'db_functions.math.test_round.RoundTests.test_integer_with_negative_precision',
        },
    }),
    ((3, 26), True, {
        'SQLite stores values rounded to 15 significant digits.': {
            'model_fields.test_decimalfield.DecimalFieldTests.test_fetch_from_db_without_float_rounding',
        },
        'SQLite naively remakes the table on field alteration.': {
            'schema.tests.SchemaTests.test_unique_no_unnecessary_fk_drops',
            'schema.tests.SchemaTests.test_unique_and_reverse_m2m',
            'schema.tests.SchemaTests.test_alter_field_default_doesnt_perform_queries',
            'schema.tests.SchemaTests.test_rename_column_renames_deferred_sql_references',
        },
        "SQLite doesn't have a constraint.": {
            'model_fields.test_integerfield.PositiveIntegerFieldTests.test_negative_values',
        },
        "SQLite doesn't support negative precision for ROUND().": {
            'db_functions.math.test_round.RoundTests.test_null_with_negative_precision',
            'db_functions.math.test_round.RoundTests.test_decimal_with_negative_precision',
            'db_functions.math.test_round.RoundTests.test_float_with_negative_precision',
            'db_functions.math.test_round.RoundTests.test_integer_with_negative_precision',
        },
        "the sqlite backend's close() method is a no-op when using an "
        "in-memory database": {
            'servers.test_liveserverthread.LiveServerThreadTest.test_closes_connections',
        },
    }),
])
def test_django_test_skips(monkeypatch, sqlite_version_info, in_memory_db, expected_skips):
    monkeypatch.setattr(DatabaseFeatures, 'connection', connection)
    monkeypatch.setattr(Database, 'sqlite_version_info', sqlite_version_info)
    monkeypatch.setattr(DatabaseFeatures.connection, 'is_in_memory_db', lambda self: in_memory_db)
    
    db_features = DatabaseFeatures()
    skips = db_features.django_test_skips()
    
    assert skips == expected_skips