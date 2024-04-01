"""
True to its name, `funccache` implements the cache function. Cache the return
value of a callable object or all methods defined in a class.

    >>> import funccache

    >>> class Alpha(metaclass=funccache):
    >>>     ...

    >>> @funccache
    >>> def alpha():
    >>>     ...

    @version: 2.0alpha1
    @author: 竹永康 <gqylpy@outlook.com>
    @source: https://github.com/gqylpy/funccache

────────────────────────────────────────────────────────────────────────────────
Copyright (c) 2022-2024 GQYLPY <http://gqylpy.com>. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from typing import Optional, Union, Callable


def ttl(x: Optional[Union[str, int, float]] = None, /) -> Callable:
    """Decorator, can specify the cache time to live by the parameter `x`, less
    than or equal to 0 means immediate expiration, default never expires."""


def count(x: Optional[int] = None, /) -> Callable:
    """Decorator, cache according to the number of calls. Whenever the number of
    calls reaches `x`, the cache will be invalidated, round by round. Less than
    or equal to 0 means immediate expiration, default never expires."""


def clear_cache_pool(func: Callable, /) -> None:
    """Clear the cache pool for the specified function or object or class."""
    func.__cache_pool__.clear()


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    import sys

    gcode = __import__(f'{__name__}.i {__name__}', fromlist=...)
    FuncCache = gcode.FuncCache

    for gname, gvalue in globals().items():
        if gname[0] == '_' and gname != '__builtins__':
            setattr(FuncCache, gname, gvalue)

    FuncCache.__module__       = __package__
    FuncCache.FuncCache        = FuncCache
    FuncCache.ttl              = gcode.FunctionCallerTTL
    FuncCache.count            = gcode.FunctionCallerCount
    FuncCache.clear_cache_pool = gcode.clear_cache_pool

    sys.modules[__name__] = FuncCache
