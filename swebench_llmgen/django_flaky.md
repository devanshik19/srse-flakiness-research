# Django — Flaky LLM-Generated Tests

Flaky tests found in the gpt-4o-mini-generated Django test suite (SWE-bench Verified, 20-instance
sample). A test is **flaky** if its verdict (PASSED/FAILED/ERROR) is not identical across repeated
runs of the same suite.

## How they were found

Each instance's generated tests were run as a **suite** (`pytest` over the whole instance folder,
sharing one migrated in-memory Django test DB) 10x in each of six regimes:

- `baseline` — fixed test order, no stress
- `cpu` / `io` / `memory` — fixed order, under stress-ng load
- `shuffle` — **random test order + random `PYTHONHASHSEED`** each run (via pytest-randomly)

The column "flips in" lists the regime(s) where the verdict changed run-to-run.

## Result

- **75 flaky functions / 895 (8.4%)**, across **30 files / 273**.
- **shuffle: 69** (order-dependent — tests reuse DB identities like `username='testuser'` and
  collide depending on order), **baseline: 8** (intrinsic — random `PYTHONHASHSEED` changes dict/set
  iteration order), **cpu: 2, io: 2, memory: 0** (resource stress finds ~nothing).
- Verified: a flaky file run **in isolation** is stable → the flakiness is order-dependence, not
  intrinsic, for the shuffle group.

## Flaky tests (linked to source)


### django__django-11087

| test | flips in |
|---|---|
| [`test_add_field_update__0.py`](flaky_tests/django/django__django-11087/test_add_field_update__0.py) :: `TestCollector::test_add_field_update_with_different_fields` | shuffle |
| [`test_add_field_update__0.py`](flaky_tests/django/django__django-11087/test_add_field_update__0.py) :: `TestCollector::test_add_field_update_with_multiple_objects` | shuffle |
| [`test_add_field_update__0.py`](flaky_tests/django/django__django-11087/test_add_field_update__0.py) :: `TestCollector::test_add_field_update_with_single_object` | shuffle |
| [`test_add_field_update__3.py`](flaky_tests/django/django__django-11087/test_add_field_update__3.py) :: `test_add_field_update_multiple_objects` | shuffle |
| [`test_add_field_update__3.py`](flaky_tests/django/django__django-11087/test_add_field_update__3.py) :: `test_add_field_update_single_object` | shuffle |
| [`test_add_field_update__4.py`](flaky_tests/django/django__django-11087/test_add_field_update__4.py) :: `test_add_field_update` | shuffle |
| [`test_add_field_update__5.py`](flaky_tests/django/django__django-11087/test_add_field_update__5.py) :: `test_add_field_update` | shuffle |
| [`test_add_field_update__7.py`](flaky_tests/django/django__django-11087/test_add_field_update__7.py) :: `test_add_field_update_with_non_empty_objs` | shuffle |
| [`test_add_field_update__7.py`](flaky_tests/django/django__django-11087/test_add_field_update__7.py) :: `test_add_field_update_with_single_user` | shuffle |
| [`test_add_field_update__8.py`](flaky_tests/django/django__django-11087/test_add_field_update__8.py) :: `test_add_field_update_with_different_field_value` | shuffle |
| [`test_add_field_update__8.py`](flaky_tests/django/django__django-11087/test_add_field_update__8.py) :: `test_add_field_update_with_homogeneous_objects` | shuffle |
| [`test_can_fast_delete__0.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__0.py) :: `test_can_fast_delete_no_signals` | shuffle |
| [`test_can_fast_delete__1.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__1.py) :: `test_can_fast_delete_no_signals[None-False]` | shuffle |
| [`test_can_fast_delete__1.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__1.py) :: `test_can_fast_delete_with_signals` | shuffle |
| [`test_can_fast_delete__3.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__3.py) :: `test_can_fast_delete_with_pre_delete_listener` | shuffle |
| [`test_can_fast_delete__4.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__4.py) :: `test_can_fast_delete_with_generic_foreign_key` | shuffle |
| [`test_can_fast_delete__4.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__4.py) :: `test_can_fast_delete_with_signal_listeners` | shuffle |
| [`test_can_fast_delete__5.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__5.py) :: `test_can_fast_delete_with_bulk_related_objects` | baseline,cpu,io,shuffle |
| [`test_can_fast_delete__5.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__5.py) :: `test_can_fast_delete_with_different_on_delete_behavior` | baseline,cpu,io,shuffle |
| [`test_can_fast_delete__5.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__5.py) :: `test_can_fast_delete_with_pre_delete_listener` | shuffle |
| [`test_can_fast_delete__7.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__7.py) :: `test_can_fast_delete_no_cascade[None-False]` | shuffle |
| [`test_can_fast_delete__7.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__7.py) :: `test_can_fast_delete_with_signal_listeners[0-0-1-False]` | shuffle |
| [`test_can_fast_delete__7.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__7.py) :: `test_can_fast_delete_with_signal_listeners[0-1-0-False]` | shuffle |
| [`test_can_fast_delete__7.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__7.py) :: `test_can_fast_delete_with_signal_listeners[1-0-0-False]` | shuffle |
| [`test_can_fast_delete__8.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__8.py) :: `test_can_fast_delete_with_cascade` | shuffle |
| [`test_can_fast_delete__8.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__8.py) :: `test_can_fast_delete_with_signal_listener` | shuffle |
| [`test_collect__0.py`](flaky_tests/django/django__django-11087/test_collect__0.py) :: `test_collect_fast_delete` | shuffle |
| [`test_collect__0.py`](flaky_tests/django/django__django-11087/test_collect__0.py) :: `test_collect_nullable` | shuffle |
| [`test_collect__0.py`](flaky_tests/django/django__django-11087/test_collect__0.py) :: `test_collect_reverse_dependency` | shuffle |
| [`test_collect__0.py`](flaky_tests/django/django__django-11087/test_collect__0.py) :: `test_collect_with_keep_parents` | shuffle |
| [`test_collect__0.py`](flaky_tests/django/django__django-11087/test_collect__0.py) :: `test_collect_with_parents` | shuffle |
| [`test_collect__1.py`](flaky_tests/django/django__django-11087/test_collect__1.py) :: `test_collect_fast_delete` | shuffle |
| [`test_collect__1.py`](flaky_tests/django/django__django-11087/test_collect__1.py) :: `test_collect_keep_parents` | shuffle |
| [`test_collect__1.py`](flaky_tests/django/django__django-11087/test_collect__1.py) :: `test_collect_no_new_objs` | shuffle |
| [`test_collect__1.py`](flaky_tests/django/django__django-11087/test_collect__1.py) :: `test_collect_with_relation` | shuffle |
| [`test_collect__2.py`](flaky_tests/django/django__django-11087/test_collect__2.py) :: `TestCollector::test_collect_fast_delete` | shuffle |
| [`test_collect__2.py`](flaky_tests/django/django__django-11087/test_collect__2.py) :: `TestCollector::test_collect_no_fast_delete` | shuffle |
| [`test_collect__2.py`](flaky_tests/django/django__django-11087/test_collect__2.py) :: `TestCollector::test_collect_reverse_dependency` | shuffle |
| [`test_collect__2.py`](flaky_tests/django/django__django-11087/test_collect__2.py) :: `TestCollector::test_collect_with_keep_parents` | shuffle |
| [`test_collect__2.py`](flaky_tests/django/django__django-11087/test_collect__2.py) :: `TestCollector::test_collect_with_nullable` | shuffle |
| [`test_collect__2.py`](flaky_tests/django/django__django-11087/test_collect__2.py) :: `TestCollector::test_collect_with_related_objects` | shuffle |
| [`test_collect__3.py`](flaky_tests/django/django__django-11087/test_collect__3.py) :: `test_collect_fast_delete` | shuffle |
| [`test_collect__3.py`](flaky_tests/django/django__django-11087/test_collect__3.py) :: `test_collect_keep_parents` | shuffle |
| [`test_collect__4.py`](flaky_tests/django/django__django-11087/test_collect__4.py) :: `test_collect_fast_delete` | shuffle |
| [`test_collect__4.py`](flaky_tests/django/django__django-11087/test_collect__4.py) :: `test_collect_related_objects` | shuffle |
| [`test_collect__4.py`](flaky_tests/django/django__django-11087/test_collect__4.py) :: `test_collect_with_keep_parents` | shuffle |
| [`test_collect__4.py`](flaky_tests/django/django__django-11087/test_collect__4.py) :: `test_collect_with_parents` | shuffle |
| [`test_collect__5.py`](flaky_tests/django/django__django-11087/test_collect__5.py) :: `test_collect_fast_delete` | shuffle |
| [`test_collect__5.py`](flaky_tests/django/django__django-11087/test_collect__5.py) :: `test_collect_keep_parents` | shuffle |
| [`test_collect__5.py`](flaky_tests/django/django__django-11087/test_collect__5.py) :: `test_collect_non_fast_delete` | shuffle |
| [`test_collect__5.py`](flaky_tests/django/django__django-11087/test_collect__5.py) :: `test_collect_with_related` | shuffle |
| [`test_collect__8.py`](flaky_tests/django/django__django-11087/test_collect__8.py) :: `test_collect[True-False-False]` | shuffle |
| [`test_collect__9.py`](flaky_tests/django/django__django-11087/test_collect__9.py) :: `TestCollector::test_collect_with_fast_delete` | shuffle |
| [`test_collect__9.py`](flaky_tests/django/django__django-11087/test_collect__9.py) :: `TestCollector::test_collect_with_related_objects` | shuffle |

### django__django-11141

| test | flips in |
|---|---|
| [`test_load_disk__1.py`](flaky_tests/django/django__django-11141/test_load_disk__1.py) :: `test_load_disk_no_migrations` | baseline |
| [`test_load_disk__1.py`](flaky_tests/django/django__django-11141/test_load_disk__1.py) :: `test_load_disk_with_migrations` | baseline |
| [`test_load_disk__3.py`](flaky_tests/django/django__django-11141/test_load_disk__3.py) :: `TestMigrationLoader::test_load_disk_no_migrations` | baseline |
| [`test_load_disk__8.py`](flaky_tests/django/django__django-11141/test_load_disk__8.py) :: `TestMigrationLoader::test_load_disk_import_error` | baseline |
| [`test_load_disk__8.py`](flaky_tests/django/django__django-11141/test_load_disk__8.py) :: `TestMigrationLoader::test_load_disk_no_migration_module` | baseline |
| [`test_load_disk__8.py`](flaky_tests/django/django__django-11141/test_load_disk__8.py) :: `TestMigrationLoader::test_load_disk_valid_migrations` | baseline |

### django__django-11163

| test | flips in |
|---|---|
| [`test_model_to_dict__1.py`](flaky_tests/django/django__django-11163/test_model_to_dict__1.py) :: `test_model_to_dict_with_all_fields` | shuffle |
| [`test_model_to_dict__3.py`](flaky_tests/django/django__django-11163/test_model_to_dict__3.py) :: `test_model_to_dict_no_editable_fields` | shuffle |
| [`test_model_to_dict__5.py`](flaky_tests/django/django__django-11163/test_model_to_dict__5.py) :: `test_model_to_dict_no_fields` | shuffle |
| [`test_model_to_dict__7.py`](flaky_tests/django/django__django-11163/test_model_to_dict__7.py) :: `test_model_to_dict_with_fields` | shuffle |
| [`test_model_to_dict__7.py`](flaky_tests/django/django__django-11163/test_model_to_dict__7.py) :: `test_model_to_dict_with_no_fields` | shuffle |

### django__django-11206

| test | flips in |
|---|---|
| [`test_format__6.py`](flaky_tests/django/django__django-11206/test_format__6.py) :: `test_format_decimal_with_grouping` | shuffle |
| [`test_format__6.py`](flaky_tests/django/django__django-11206/test_format__6.py) :: `test_format_decimal_with_position` | shuffle |
| [`test_format__6.py`](flaky_tests/django/django__django-11206/test_format__6.py) :: `test_format_integer_with_grouping` | shuffle |
| [`test_format__6.py`](flaky_tests/django/django__django-11206/test_format__6.py) :: `test_format_negative_decimal_with_grouping` | shuffle |
| [`test_format__6.py`](flaky_tests/django/django__django-11206/test_format__6.py) :: `test_format_negative_integer_with_grouping` | shuffle |
| [`test_format__6.py`](flaky_tests/django/django__django-11206/test_format__6.py) :: `test_format_no_decimal_sep` | shuffle |
| [`test_format__8.py`](flaky_tests/django/django__django-11206/test_format__8.py) :: `test_format_float_with_custom_thousand_sep` | shuffle |
| [`test_format__8.py`](flaky_tests/django/django__django-11206/test_format__8.py) :: `test_format_float_with_grouping` | shuffle |
| [`test_format__8.py`](flaky_tests/django/django__django-11206/test_format__8.py) :: `test_format_integer_with_grouping` | shuffle |
| [`test_format__8.py`](flaky_tests/django/django__django-11206/test_format__8.py) :: `test_format_negative_integer` | shuffle |
