# Django — Flaky LLM-Generated Test Files

**30 flaky test files** (of 273 that ran), from **6 focal methods**. Grouped by instance → focal method → generation run (run N = the Nth of the 10 generated samples for that method). Each run links to its test body; "flaky functions" = how many `def test_` in it flip; "flips in" = the regime(s) where flipping occurs. Regimes: baseline, cpu/io/memory stress, hashseed (random `PYTHONHASHSEED`, fixed order), order (random test order).


## django__django-11087

### focal method: `add_field_update`  (6 flaky run(s))

| run | file | flaky functions | flips in |
|---|---|---|---|
| 1 | [`test_add_field_update__0.py`](flaky_tests/django/django__django-11087/test_add_field_update__0.py) | 3 | order |
| 4 | [`test_add_field_update__3.py`](flaky_tests/django/django__django-11087/test_add_field_update__3.py) | 2 | order |
| 5 | [`test_add_field_update__4.py`](flaky_tests/django/django__django-11087/test_add_field_update__4.py) | 1 | order |
| 6 | [`test_add_field_update__5.py`](flaky_tests/django/django__django-11087/test_add_field_update__5.py) | 1 | order |
| 8 | [`test_add_field_update__7.py`](flaky_tests/django/django__django-11087/test_add_field_update__7.py) | 2 | order |
| 9 | [`test_add_field_update__8.py`](flaky_tests/django/django__django-11087/test_add_field_update__8.py) | 2 | order |

### focal method: `can_fast_delete`  (7 flaky run(s))

| run | file | flaky functions | flips in |
|---|---|---|---|
| 1 | [`test_can_fast_delete__0.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__0.py) | 1 | order |
| 2 | [`test_can_fast_delete__1.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__1.py) | 2 | order |
| 4 | [`test_can_fast_delete__3.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__3.py) | 1 | order |
| 5 | [`test_can_fast_delete__4.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__4.py) | 2 | order |
| 6 | [`test_can_fast_delete__5.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__5.py) | 3 | hashseed,order |
| 8 | [`test_can_fast_delete__7.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__7.py) | 4 | order |
| 9 | [`test_can_fast_delete__8.py`](flaky_tests/django/django__django-11087/test_can_fast_delete__8.py) | 2 | order |

### focal method: `collect`  (8 flaky run(s))

| run | file | flaky functions | flips in |
|---|---|---|---|
| 1 | [`test_collect__0.py`](flaky_tests/django/django__django-11087/test_collect__0.py) | 5 | order |
| 2 | [`test_collect__1.py`](flaky_tests/django/django__django-11087/test_collect__1.py) | 4 | order |
| 3 | [`test_collect__2.py`](flaky_tests/django/django__django-11087/test_collect__2.py) | 6 | order |
| 4 | [`test_collect__3.py`](flaky_tests/django/django__django-11087/test_collect__3.py) | 2 | order |
| 5 | [`test_collect__4.py`](flaky_tests/django/django__django-11087/test_collect__4.py) | 4 | order |
| 6 | [`test_collect__5.py`](flaky_tests/django/django__django-11087/test_collect__5.py) | 4 | order |
| 9 | [`test_collect__8.py`](flaky_tests/django/django__django-11087/test_collect__8.py) | 1 | order |
| 10 | [`test_collect__9.py`](flaky_tests/django/django__django-11087/test_collect__9.py) | 2 | order |


## django__django-11141

### focal method: `load_disk`  (3 flaky run(s))

| run | file | flaky functions | flips in |
|---|---|---|---|
| 2 | [`test_load_disk__1.py`](flaky_tests/django/django__django-11141/test_load_disk__1.py) | 2 | baseline |
| 4 | [`test_load_disk__3.py`](flaky_tests/django/django__django-11141/test_load_disk__3.py) | 1 | baseline |
| 9 | [`test_load_disk__8.py`](flaky_tests/django/django__django-11141/test_load_disk__8.py) | 3 | baseline |


## django__django-11163

### focal method: `model_to_dict`  (4 flaky run(s))

| run | file | flaky functions | flips in |
|---|---|---|---|
| 2 | [`test_model_to_dict__1.py`](flaky_tests/django/django__django-11163/test_model_to_dict__1.py) | 1 | order |
| 4 | [`test_model_to_dict__3.py`](flaky_tests/django/django__django-11163/test_model_to_dict__3.py) | 1 | order |
| 6 | [`test_model_to_dict__5.py`](flaky_tests/django/django__django-11163/test_model_to_dict__5.py) | 1 | order |
| 8 | [`test_model_to_dict__7.py`](flaky_tests/django/django__django-11163/test_model_to_dict__7.py) | 2 | order |


## django__django-11206

### focal method: `format`  (2 flaky run(s))

| run | file | flaky functions | flips in |
|---|---|---|---|
| 7 | [`test_format__6.py`](flaky_tests/django/django__django-11206/test_format__6.py) | 6 | order |
| 9 | [`test_format__8.py`](flaky_tests/django/django__django-11206/test_format__8.py) | 4 | order |

