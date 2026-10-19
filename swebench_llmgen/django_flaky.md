# Django — Flaky LLM-Generated Test Files

**30 flaky test files** (of 273 that ran) from the gpt-4o-mini-generated Django suite, SWE-bench
Verified 20-instance sample. A file is flaky if any of its test functions changes verdict across
repeated runs. Each file is linked to its body; "flaky functions" = how many `def test_` in it flip;
"flips in" = the regime(s) where flipping occurs. Regimes: baseline, cpu/io/memory stress, and
shuffle (random test order + random `PYTHONHASHSEED`).

## Flaky files


### django__django-11087

| file | flaky functions | flips in |
|---|---|---|
| [`test_add_field_update__0.py`](flaky_tests/django/django__django-11087/test_add_field_update__0.py) | 3 | shuffle |
| [`test_add_field_update__3.py`](flaky_tests/django/django__django-11087/test_add_field_update__3.py) | 2 | shuffle |
| [`test_add_field_update__4.py`](flaky_tests/django/django__django-11087/test_add_field_update__4.py) | 1 | shuffle |
| [`test_add_field_update__5.py`](flaky_tests/django/django__django-11087/test_add_field_update__5.py) | 1 | shuffle |
| [`test_add_field_update__7.py`](flaky_tests/django/django__django-11087/test_add_field_update__7.py) | 2 | shuffle |
| [`test_add_field_update__8.py`](flaky_tests/django/django__django-11087/test_add_field_update__8.py) | 2 | shuffle |
| [`test_can_fast_delete__0.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__0.py) | 1 | shuffle |
| [`test_can_fast_delete__1.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__1.py) | 2 | shuffle |
| [`test_can_fast_delete__3.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__3.py) | 1 | shuffle |
| [`test_can_fast_delete__4.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__4.py) | 2 | shuffle |
| [`test_can_fast_delete__5.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__5.py) | 3 | baseline,cpu,io,shuffle |
| [`test_can_fast_delete__7.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__7.py) | 4 | shuffle |
| [`test_can_fast_delete__8.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__8.py) | 2 | shuffle |
| [`test_collect__0.py`](flaky_tests/django/django__django-11087/test_collect__0.py) | 5 | shuffle |
| [`test_collect__1.py`](flaky_tests/django/django__django-11087/test_collect__1.py) | 4 | shuffle |
| [`test_collect__2.py`](flaky_tests/django/django__django-11087/test_collect__2.py) | 6 | shuffle |
| [`test_collect__3.py`](flaky_tests/django/django__django-11087/test_collect__3.py) | 2 | shuffle |
| [`test_collect__4.py`](flaky_tests/django/django__django-11087/test_collect__4.py) | 4 | shuffle |
| [`test_collect__5.py`](flaky_tests/django/django__django-11087/test_collect__5.py) | 4 | shuffle |
| [`test_collect__8.py`](flaky_tests/django/django__django-11087/test_collect__8.py) | 1 | shuffle |
| [`test_collect__9.py`](flaky_tests/django/django__django-11087/test_collect__9.py) | 2 | shuffle |

### django__django-11141

| file | flaky functions | flips in |
|---|---|---|
| [`test_load_disk__1.py`](flaky_tests/django/django__django-11141/test_load_disk__1.py) | 2 | baseline |
| [`test_load_disk__3.py`](flaky_tests/django/django__django-11141/test_load_disk__3.py) | 1 | baseline |
| [`test_load_disk__8.py`](flaky_tests/django/django__django-11141/test_load_disk__8.py) | 3 | baseline |

### django__django-11163

| file | flaky functions | flips in |
|---|---|---|
| [`test_model_to_dict__1.py`](flaky_tests/django/django__django-11163/test_model_to_dict__1.py) | 1 | shuffle |
| [`test_model_to_dict__3.py`](flaky_tests/django/django__django-11163/test_model_to_dict__3.py) | 1 | shuffle |
| [`test_model_to_dict__5.py`](flaky_tests/django/django__django-11163/test_model_to_dict__5.py) | 1 | shuffle |
| [`test_model_to_dict__7.py`](flaky_tests/django/django__django-11163/test_model_to_dict__7.py) | 2 | shuffle |

### django__django-11206

| file | flaky functions | flips in |
|---|---|---|
| [`test_format__6.py`](flaky_tests/django/django__django-11206/test_format__6.py) | 6 | shuffle |
| [`test_format__8.py`](flaky_tests/django/django__django-11206/test_format__8.py) | 4 | shuffle |
