"""
    A global cache object for frequently consistent grabbed database items

    Use the get function only and provide a way to set the object if it does not exist in the cache.
"""

import time

_EXPIRE_TIME_SECONDS = 60*10    # Ten minutes
_CACHE = {
    # (timestamp, value)
}


def _set(key, value):
    _CACHE[key] = (time.time(), value)


def get(key, get_func, *get_func_args, **get_func_kwargs):
    if key not in _CACHE or (time.time() - _CACHE[key][0]) >= _EXPIRE_TIME_SECONDS:
        _set(key, get_func(*get_func_args, **get_func_kwargs))
    return _CACHE[key][1]
