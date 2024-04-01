"""
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
import re
import time
import asyncio
import threading
import functools

from types import MethodType, FunctionType

from typing import (
    TypeVar, Type, Optional, Union, Dict, List, Tuple, Set, Iterable, Callable,
    FrozenSet, Any
)

try:
    from typing import TypeAlias
except ImportError:
    TypeAlias = ...

MethodTypeOrName: TypeAlias = TypeVar('MethodTypeOrName', MethodType, str)
Closure:          TypeAlias = TypeVar('Closure', bound=Callable)

MethodCachePool: TypeAlias = Dict[
    Union[Tuple[str, Tuple[Tuple[Any, ...], FrozenSet[Tuple[str, Any]]]], str],
    Dict[str, Any]
]

FuncCachePool: TypeAlias = Dict[
    Tuple[Tuple[Any, ...], FrozenSet[Tuple[str, Any]]],
    Dict[str, Any]
]


class FuncCache(type):
    __shared_instance_cache__: bool                   = False
    __not_cache__:             List[MethodTypeOrName] = []
    __ttl__:                   Union[str, int, float] = float('inf')

    def __new__(
            mcs, __name__: Union[str, FunctionType, Type[object]], *a, **kw
    ) -> Union['FuncCache', 'FunctionCaller']:
        if isinstance(__name__, (FunctionType, type)):
            return FunctionCaller(__name__)
        return type.__new__(mcs, __name__, *a, **kw)

    def __init__(cls, __name__: str, __bases__: tuple, __dict__: dict):
        __not_cache__: List[MethodTypeOrName] = __dict__.get('__not_cache__')

        if __not_cache__:
            cls.dedup(__not_cache__)
            cls.check_and_tidy_not_cache(__not_cache__)
            cls.dedup(__not_cache__)

        assert '__getattribute__' not in __dict__, \
            f'instances of "{FuncCache.__name__}" are not allowed to define ' \
            'method "__getattribute__".'

        cls.__getattribute__ = __getattribute__(cls)

        if cls.__shared_instance_cache__:
            cls.__primary_lock__ = threading.Lock()
            cls.__cache_pool__: MethodCachePool = {}

        cls.__ttl__ = Time2Second(cls.__ttl__)

        type.__init__(cls, __name__, __bases__, __dict__)

    def __call__(cls, *a, **kw):
        ins: cls = type.__call__(cls, *a, **kw)

        if not cls.__shared_instance_cache__:
            ins.__primary_lock__ = threading.Lock()
            ins.__cache_pool__ = {}

        return ins

    def check_and_tidy_not_cache(
            cls, __not_cache__: List[MethodTypeOrName], /
    ) -> None:
        not_found: Set[str] = set()

        for index, name_or_method in enumerate(__not_cache__):
            if name_or_method.__class__ is str:
                name: str = name_or_method

                for x in cls.local_instance_dict_set():
                    if name == x:
                        break
                else:
                    not_found.add(name)
                    continue

                method: MethodType = getattr(cls, name)

            else:
                method: MethodType = name_or_method

                try:
                    name = __not_cache__[index] = method.__name__
                except AttributeError:
                    if method.__class__ in (staticmethod, classmethod):
                        name = __not_cache__[index] = method.__func__.__name__
                    elif method.__class__ is property:
                        name = __not_cache__[index] = method.fget.__name__
                    else:
                        name = name_or_method

                for x in cls.local_instance_dict_set(v=True):
                    if method == x:
                        break
                else:
                    not_found.add(name)
                    continue

            if not (
                    callable(method)
                    or method.__class__ in (property, staticmethod, classmethod)
            ):
                not_found.add(name)
                continue

        if not_found:
            x = f'{cls.__module__}.{cls.__name__}'
            y = not_found if len(not_found) > 1 else not_found.pop()
            raise type(
                'NotCacheDefineError', (Exception,), {'__module__': __package__}
            )(f'"{__package__}" instance "{x}" has no method "{y}".')

    @staticmethod
    def dedup(data: List[Any]) -> None:
        index = len(data) - 1
        while index > -1:
            offset = -1
            while index + offset > -1:
                if data[index + offset] == data[index]:
                    del data[index]
                    break
                else:
                    offset -= 1
            index -= 1

    def local_instance_dict_set(
            cls, baseclass: Optional['FuncCache'] = None, /, *, v: bool = False
    ) -> Iterable[MethodTypeOrName]:
        cur_cls: FuncCache = baseclass or cls

        if cur_cls.__class__ is FuncCache:
            yield from cur_cls.__dict__.values() if v else cur_cls.__dict__
            yield from cur_cls.local_instance_dict_set(cur_cls.__base__)


class MethodCaller:

    def __new__(
            cls,
            cls_:   FuncCache,
            sget:   Callable[[str], Any],
            name:   str,
            method: Union[MethodType, property]
    ) -> Any:
        if method.__class__ is not property:
            return object.__new__(cls)

        __cache_pool__: MethodCachePool = sget('__cache_pool__')
        cache: Dict[str, Any] = __cache_pool__.get(name)

        if not cache:
            with sget('__primary_lock__'):
                if name in __cache_pool__:
                    cache: Dict[str, Any] = __cache_pool__[name]
                else:
                    cache = __cache_pool__[name] = {
                        '__secondary_lock__': threading.Lock(),
                        '__expiration_time__': 0
                    }

        if cache['__expiration_time__'] < time.time():
            with cache['__secondary_lock__']:
                if cache['__expiration_time__'] < time.time():
                    cache['__return__'] = sget(name)
                    cache['__expiration_time__'] = time.time() + cls_.__ttl__

        return cache['__return__']

    def __init__(
            self,
            cls:    FuncCache,
            sget:   Callable[[str], Any],
            name:   str,
            method: MethodType
    ):
        self.__cls        = cls
        self.__sget       = sget
        self.__name__     = name
        self.__func__     = method
        self.__qualname__ = method.__qualname__

    def __call__(self, *a, **kw) -> Any:
        key = self.__name__, (a, frozenset(kw.items()))

        __cache_pool__: MethodCachePool = self.__sget('__cache_pool__')
        cache: Dict[str, Any] = __cache_pool__.get(key)

        if not cache:
            with self.__sget('__primary_lock__'):
                if key in __cache_pool__:
                    cache: Dict[str, Any] = __cache_pool__[key]
                else:
                    cache = __cache_pool__[key] = {
                        '__secondary_lock__': threading.Lock(),
                        '__expiration_time__': 0
                    }

        if cache['__expiration_time__'] < time.time():
            with cache['__secondary_lock__']:
                if cache['__expiration_time__'] < time.time():
                    cache['__return__'] = self.__sget(self.__name__)(*a, **kw)
                    cache['__expiration_time__'] = \
                        time.time() + self.__cls.__ttl__

        return cache['__return__']

    def __str__(self) -> str:
        return f'{MethodCaller.__name__}' \
               f'({self.__cls.__module__}.{self.__qualname__})'


class FunctionCaller:

    def __init__(self, func: FunctionType, /):
        self.__func__ = func

        if func.__class__ is FunctionType:
            self.__globals__ = func.__globals__
            functools.wraps(func)(self)

            if asyncio.iscoroutinefunction(getattr(func, '__wrapped__', func)):
                self.core = self.acore

        self.__primary_lock__ = threading.Lock()
        self.__cache_pool__: FuncCachePool = {}

    def __call__(self, *a, **kw) -> Any:
        return self.core(*a, **kw)

    def __str__(self) -> str:
        return str(self.__func__)

    def core(self, *a, **kw) -> Any:
        key = a, frozenset(kw.items())

        try:
            cache: Dict[str, Any] = self.__cache_pool__[key]
        except KeyError:
            with self.__primary_lock__:
                if key in self.__cache_pool__:
                    cache: Dict[str, Any] = self.__cache_pool__[key]
                else:
                    cache = self.__cache_pool__[key] = \
                        {'__secondary_lock__': threading.Lock()}

        try:
            result: Any = cache['__return__']
        except KeyError:
            with cache['__secondary_lock__']:
                if '__return__' in cache:
                    result: Any = cache['__return__']
                else:
                    result = cache['__return__'] = self.__func__(*a, **kw)
                    del cache['__secondary_lock__']

        return result

    async def acore(self, *a, **kw) -> Any:
        key = a, frozenset(kw.items())

        try:
            cache: Dict[str, Any] = self.__cache_pool__[key]
        except KeyError:
            with self.__primary_lock__:
                if key in self.__cache_pool__:
                    cache: Dict[str, Any] = self.__cache_pool__[key]
                else:
                    cache = self.__cache_pool__[key] = \
                        {'__secondary_lock__': threading.Lock()}

        try:
            result: Any = cache['__return__']
        except KeyError:
            with cache['__secondary_lock__']:
                if '__return__' in cache:
                    result: Any = cache['__return__']
                else:
                    result = cache['__return__'] = await self.__func__(*a, **kw)
                    del cache['__secondary_lock__']

        return result


class FunctionCallerTTL:

    def __init__(self, ttl: Optional[Union[str, int, float]] = None, /):
        if ttl is not None:
            self.__ttl = Time2Second(ttl)
        elif ttl is not None:
            self.__ttl = Time2Second(ttl)
        else:
            self.__ttl = float('inf')

        self.__primary_lock__ = threading.Lock()
        self.__cache_pool__: FuncCachePool = {}

    def __call__(self, func: FunctionType, /) -> Closure:
        self.__func__ = func

        if asyncio.iscoroutinefunction(getattr(func, '__wrapped__', func)):
            self.core = self.acore

        @functools.wraps(func, updated=('__dict__', '__globals__'))
        def inner(*a, **kw) -> Any:
            return self.core(func, *a, **kw)

        inner.__cache_pool__ = self.__cache_pool__

        return inner

    def core(self, func: FunctionType, /, *a, **kw) -> Any:
        key = a, frozenset(kw.items())

        cache: Dict[str, Any] = self.__cache_pool__.get(key)

        if not cache:
            with self.__primary_lock__:
                if key not in self.__cache_pool__:
                    cache = self.__cache_pool__[key] = {
                        '__secondary_lock__': threading.Lock(),
                        '__expiration_time__': 0
                    }

        if cache['__expiration_time__'] < time.time():
            with cache['__secondary_lock__']:
                if cache['__expiration_time__'] < time.time():
                    cache['__return__'] = func(*a, **kw)
                    cache['__expiration_time__'] = time.time() + self.__ttl

        return cache['__return__']

    async def acore(self, func: FunctionType, /, *a, **kw) -> Any:
        key = a, frozenset(kw.items())

        cache: Dict[str, Any] = self.__cache_pool__.get(key)

        if not cache:
            with self.__primary_lock__:
                if key not in self.__cache_pool__:
                    cache = self.__cache_pool__[key] = {
                        '__secondary_lock__': threading.Lock(),
                        '__expiration_time__': 0
                    }

        if cache['__expiration_time__'] < time.time():
            with cache['__secondary_lock__']:
                if cache['__expiration_time__'] < time.time():
                    cache['__return__'] = await func(*a, **kw)
                    cache['__expiration_time__'] = time.time() + self.__ttl

        return cache['__return__']


class FunctionCallerCount:

    def __init__(self, count: int = 0, /):
        if count.__class__ is not int:
            x: str = count.__class__.__name__
            raise TypeError(
                f'parameter "count" type must be an int, not "{x}".'
            )

        self.__count = count

        self.__primary_lock__ = threading.Lock()
        self.__cache_pool__: FuncCachePool = {}

    def __call__(self, func: FunctionType, /) -> Closure:
        self.__func__ = func

        if asyncio.iscoroutinefunction(getattr(func, '__wrapped__', func)):
            self.core = self.acore

        @functools.wraps(func, updated=('__dict__', '__globals__'))
        def inner(*a, **kw) -> Any:
            return self.core(func, *a, **kw)

        inner.__cache_pool__ = self.__cache_pool__

        return inner

    def core(self, func: FunctionType, /, *a, **kw) -> Any:
        key = a, frozenset(kw.items())

        cache: Dict[str, Any] = self.__cache_pool__.get(key)

        if not cache:
            with self.__primary_lock__:
                if key not in self.__cache_pool__:
                    cache = self.__cache_pool__[key] = {
                        '__secondary_lock__': threading.Lock(),
                        '__count__': self.__count
                    }

        if cache['__count__'] == self.__count:
            with cache['__secondary_lock__']:
                if cache['__count__'] == self.__count:
                    cache['__return__'] = func(*a, **kw)
                    cache['__count__'] = 1
        else:
            cache['__count__'] += 1

        return cache['__return__']

    async def acore(self, func: FunctionType, /, *a, **kw) -> Any:
        key = a, frozenset(kw.items())

        cache: Dict[str, Any] = self.__cache_pool__.get(key)

        if not cache:
            with self.__primary_lock__:
                if key not in self.__cache_pool__:
                    cache = self.__cache_pool__[key] = {
                        '__secondary_lock__': threading.Lock(),
                        '__count__': self.__count
                    }

        if cache['__count__'] == self.__count:
            with cache['__secondary_lock__']:
                if cache['__count__'] == self.__count:
                    cache['__return__'] = await func(*a, **kw)
                    cache['__count__'] = 1
        else:
            cache['__count__'] += 1

        return cache['__return__']


def __getattribute__(cls: FuncCache, /) -> Closure:
    def inner(ins: cls, attr: str, /) -> Any:
        sget: Callable[[str], Any] = super(cls, ins).__getattribute__

        if (
                attr in ('__cache_pool__', '__not_cache__') or
                attr in cls.__not_cache__ or
                attr not in cls.__dict__
        ):
            return sget(attr)

        value: Any = getattr(cls, attr)

        if not (callable(value) or value.__class__ in (property, classmethod)):
            return sget(attr)

        return MethodCaller(cls, sget, attr, value)

    return inner


def clear_cache_pool(func: Union[
        FunctionCaller, FunctionCallerTTL, Type[object], FuncCache
], /) -> None:
    try:
        func.__cache_pool__.clear()
    except AttributeError:
        raise TypeError(
            f'"{func.__module__}.{func.__qualname__}" is not cached.'
        ) from None


class Time2Second(
    metaclass=type('', (type,), {'__call__': lambda *a: type.__call__(*a)()})
):
    matcher = re.compile(r'''^
        (?:(\d+(?:\.\d+)?)y)?
        (?:(\d+(?:\.\d+)?)d)?
        (?:(\d+(?:\.\d+)?)h)?
        (?:(\d+(?:\.\d+)?)m)?
        (?:(\d+(?:\.\d+)?)s)?
    $''', flags=re.X | re.I)

    m = 60
    h = 60 * m
    d = 24 * h
    y = 365 * d

    def __init__(self, unit_time: Union[int, float, str], /):
        self.unit_time = unit_time

    def __call__(self) -> Union[int, float]:
        if self.unit_time.__class__ in (int, float):
            return self.unit_time
        elif self.unit_time.isdigit():
            return int(self.unit_time)
        elif '.' in self.unit_time and self.unit_time.count('.') == 1 and \
                self.unit_time.replace('.', '').isdigit():
            return float(self.unit_time)
        y, d, h, m, s = self.matcher.findall(self.unit_time)[0]
        y, d, h, m, s = self.g(y), self.g(d), self.g(h), self.g(m), self.g(s)
        return self.y * y + self.d * d + self.h * h + self.m * m + s

    @staticmethod
    def g(x: str, /) -> Union[int, float]:
        if not x:
            return 0
        try:
            return int(x)
        except ValueError:
            return float(x)
