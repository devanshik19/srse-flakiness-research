# Django — Flaky LLM-Generated Test Files

**9 flaky test files** (of 286 that ran), from **4 focal methods**. Grouped by instance → focal method → generation run (run N = the Nth of the 10 generated samples for that method). Each run links to its test body; "flaky functions" = how many `def test_` in it flip; "flips in" = the regime(s) where flipping occurs. Regimes: baseline, cpu/io/memory stress, hashseed (random `PYTHONHASHSEED`, fixed order), order (random test order).


## django__django-11333

### focal method: `reverse`  (3 flaky run(s))

| run | file | flaky functions | flips in |
|---|---|---|---|
| 5 | [`test_reverse__4.py`](flaky_tests/django/django__django-11333/test_reverse__4.py) | 2 | order |
| 8 | [`test_reverse__7.py`](flaky_tests/django/django__django-11333/test_reverse__7.py) | 3 | order |
| 9 | [`test_reverse__8.py`](flaky_tests/django/django__django-11333/test_reverse__8.py) | 1 | order |


## django__django-11433

### focal method: `construct_instance`  (4 flaky run(s))

| run | file | flaky functions | flips in |
|---|---|---|---|
| 1 | [`test_construct_instance__0.py`](flaky_tests/django/django__django-11433/test_construct_instance__0.py) | 4 | order |
| 3 | [`test_construct_instance__2.py`](flaky_tests/django/django__django-11433/test_construct_instance__2.py) | 1 | order |
| 9 | [`test_construct_instance__8.py`](flaky_tests/django/django__django-11433/test_construct_instance__8.py) | 1 | order |
| 10 | [`test_construct_instance__9.py`](flaky_tests/django/django__django-11433/test_construct_instance__9.py) | 4 | order |


## django__django-11820

### focal method: `_check_ordering`  (1 flaky run(s))

| run | file | flaky functions | flips in |
|---|---|---|---|
| 7 | [`test__check_ordering__6.py`](flaky_tests/django/django__django-11820/test__check_ordering__6.py) | 2 | order |


## django__django-11964

### focal method: `values`  (1 flaky run(s))

| run | file | flaky functions | flips in |
|---|---|---|---|
| 4 | [`test_values__3.py`](flaky_tests/django/django__django-11964/test_values__3.py) | 1 | order |

