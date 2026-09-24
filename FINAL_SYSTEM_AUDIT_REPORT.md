# Comprehensive Performance & Scalability Audit

## 1. Codebase Profiling Results
```
Sun Aug  2 21:09:02 2026    audit_profile.prof

         218088 function calls (214995 primitive calls) in 0.187 seconds

   Ordered by: cumulative time
   List reduced from 566 to 30 due to restriction <30>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.016    0.016    0.146    0.146 /app/run_profiler.py:8(run_cache_profiling)
    10000    0.017    0.000    0.073    0.000 /app/cache_manager.py:96(set)
    10000    0.020    0.000    0.057    0.000 /app/cache_manager.py:61(get)
    20000    0.021    0.000    0.054    0.000 /app/cache_manager.py:51(_generate_cache_key)
        1    0.001    0.001    0.041    0.041 /app/run_profiler.py:14(run_processor_profiling)
        1    0.000    0.000    0.039    0.039 /app/optimized_data_processor.py:20(process_menu_data)
    10000    0.025    0.000    0.027    0.000 /app/cache_manager.py:108(_prune_memory_cache)
        1    0.000    0.000    0.025    0.025 /app/optimized_data_processor.py:46(_flatten_all_items)
    20000    0.016    0.000    0.016    0.000 {method 'hexdigest' of '_hashlib.HASH' objects}
        1    0.000    0.000    0.015    0.015 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/pandas/io/json/_normalize.py:303(json_normalize)
   1001/1    0.001    0.000    0.011    0.011 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/pandas/io/json/_normalize.py:219(_simple_json_normalize)
    20000    0.010    0.000    0.010    0.000 {built-in method _hashlib.openssl_md5}
        1    0.000    0.000    0.010    0.010 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/pandas/core/frame.py:2125(to_dict)
     1000    0.004    0.000    0.010    0.000 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/pandas/io/json/_normalize.py:194(_normalize_json_ordered)
        1    0.001    0.001    0.010    0.010 /app/optimized_data_processor.py:75(_handle_remaining_nesting)
        1    0.003    0.003    0.010    0.010 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/pandas/core/methods/to_dict.py:97(to_dict)
    20000    0.006    0.000    0.006    0.000 {method 'encode' of 'str' objects}
    10000    0.004    0.000    0.006    0.000 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/logging/__init__.py:1517(debug)
    30000    0.006    0.000    0.006    0.000 {built-in method time.time}
     1000    0.000    0.000    0.006    0.000 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/json/__init__.py:183(dumps)
     1000    0.001    0.000    0.005    0.000 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/json/encoder.py:183(encode)
3000/1000    0.003    0.000    0.004    0.000 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/pandas/io/json/_normalize.py:153(_normalize_json)
18995/18983    0.004    0.000    0.004    0.000 {built-in method builtins.isinstance}
        1    0.000    0.000    0.004    0.004 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/pandas/core/frame.py:702(__init__)
     1000    0.003    0.000    0.003    0.000 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/json/encoder.py:205(iterencode)
        1    0.000    0.000    0.003    0.003 /app/optimized_data_processor.py:191(_normalize_data)
        1    0.000    0.000    0.003    0.003 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/pandas/core/internals/construction.py:463(nested_data_to_arrays)
        1    0.000    0.000    0.003    0.003 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/pandas/core/internals/construction.py:759(to_arrays)
     2027    0.001    0.000    0.002    0.000 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/pandas/core/arrays/base.py:559(__iter__)
     2000    0.002    0.000    0.002    0.000 /home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/pandas/core/dtypes/cast.py:186(maybe_box_native)



```

## 2. Performance Benchmarking
### Latency & Throughput
- **test_cache_manager_concurrency**: 0.029623196419353712 seconds mean latency
- **test_optimized_processor_flattening**: 0.03118645280645274 seconds mean latency


## 3. Deep Testing & Edge Cases
- **Concurrency**: Concurrency tests confirmed thread-safety but highlighted the overhead of Python threading under a GIL in memory management scenarios. Cache hit accuracy under high load was validated.

## 4. Scalability Analytics
- The application relies heavily on local state for the CacheManager and threading in memory. True horizontal elasticity will require replacing the local memory dict with a distributed KV store.

## Before vs. After Optimization Projections
- **Before**: System relies on local memory and thread pools.
- **After**: Migrating CacheManager to Redis allows multiple nodes to process slugs safely without duplicating API hits.
