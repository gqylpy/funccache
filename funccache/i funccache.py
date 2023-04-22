"""
Copyright (c) 2022, 2023 GQYLPY <http://gqylpy.com>. All rights reserved.

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
import time
import asyncio
import threading
import functools

FunctionType: type = threading.setprofile.__class__


class FuncCache(type):
    __shared_instance_cache__ = False
    __not_cache__ = []

    def __new__(mcs, __name__: str, *a, **kw):
        if isinstance(__name__, (FunctionType, type)):
            return FunctionCaller(__name__)
        return type.__new__(mcs, __name__, *a, **kw)

    def __init__(cls, __name__: str, __bases__: tuple, __dict__: dict):
        __not_cache__: list = __dict__.get('__not_cache__')

        if __not_cache__:
            cls.delete_repeated(__not_cache__)
            cls.check_and_tidy_not_cache(__not_cache__, __dict__)
            cls.delete_repeated(__not_cache__)

        cls.__getattribute__ = __getattribute__(cls)

        if cls.__shared_instance_cache__:
            cls.__cache_pool__ = {}

        type.__init__(cls, __name__, __bases__, __dict__)

    def __call__(cls, *a, **kw):
        ins: cls = type.__call__(cls, *a, **kw)

        if not cls.__shared_instance_cache__:
            ins.__cache_pool__ = {}

        return ins

    def check_and_tidy_not_cache(cls, __not_cache__: list, __dict__: dict):
        not_found = []

        for index, name_or_method in enumerate(__not_cache__):
            if name_or_method.__class__ is str:
                name: str = name_or_method

                for x in cls.local_instance_dict_set():
                    if name == x:
                        break
                else:
                    name in not_found or not_found.append(name)
                    continue

                method = getattr(cls, name)

            else:
                method = name_or_method

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
                    name in not_found or not_found.append(name)
                    continue

            if not (
                    callable(method)
                    or method.__class__ in (property, staticmethod, classmethod)
            ):
                name in not_found or not_found.append(name)
                continue

        if not_found:
            x = f'{cls.__module__}.{cls.__name__}'
            e = not_found if len(not_found) > 1 else not_found[0]
            raise type(
                'NotCacheDefineError', (Exception,), {'__module__': __package__}
            )(f'"{__package__}" instance "{x}" has no method "{e}".')

    @staticmethod
    def delete_repeated(data: list):
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

    def local_instance_dict_set(cls, baseclass=None, *, v: bool = False):
        cur_cls: FuncCache or type = baseclass or cls

        if cur_cls.__class__ is FuncCache:
            yield from cur_cls.__dict__.values() if v else cur_cls.__dict__
            yield from cur_cls.local_instance_dict_set(cur_cls.__base__)

    class NotCacheDefineError(Exception):
        __module__ = __package__


class ClassMethodCaller:

    def __new__(cls, cls_: FuncCache, sget, name: str, method):
        if method.__class__ is property:
            __cache_pool__: dict = sget('__cache_pool__')

            try:
                cache: dict = __cache_pool__[name]
            except KeyError:
                cache = __cache_pool__[name] = {}
                cache['__exec_lock__'] = threading.Event()
                try:
                    cache['__return__'] = sget(name)
                except Exception as e:
                    del __cache_pool__[name]
                    raise e from None
                finally:
                    cache['__exec_lock__'].set()
            else:
                if '__exec_lock__' in cache:
                    cache['__exec_lock__'].wait()
                    try:
                        del cache['__exec_lock__']
                    except KeyError:
                        pass

            return cache['__return__']

        return object.__new__(cls)

    def __init__(self, cls: FuncCache, sget, name: str, method):
        self.__cls = cls
        self.__sget = sget
        self.__name__ = name
        self.__func__ = method
        self.__qualname__ = method.__qualname__

    def __call__(self, *a, **kw):
        __cache_pool__: dict = self.__sget('__cache_pool__')
        key = self.__name__, a, str(kw)

        try:
            cache: dict = __cache_pool__[key]
        except KeyError:
            cache = __cache_pool__[key] = {}
            cache['__exec_lock__'] = threading.Event()
            cache['__return__'] = self.__sget(self.__name__)(*a, **kw)
            cache['__exec_lock__'].set()
        else:
            if '__exec_lock__' in cache:
                cache['__exec_lock__'].wait()
                try:
                    del cache['__exec_lock__']
                except KeyError:
                    pass

        return cache['__return__']

    def __str__(self):
        return f'{ClassMethodCaller.__name__}' \
               f'({self.__cls.__module__}.{self.__qualname__})'


class FunctionCaller:

    def __init__(self, func: FunctionType):
        self.__func__ = func

        if func.__class__ is FunctionType:
            self.__globals__ = func.__globals__
            functools.wraps(self.__func__)(self)

            if asyncio.iscoroutinefunction(getattr(func, '__wrapped__', func)):
                self.__core__ = self.__core_async__

        self.__exec_lock__  = threading.Lock()
        self.__cache_pool__ = {}

    def __call__(self, *a, **kw):
        return self.__core__(*a, **kw)

    def __core__(self, *a, **kw):
        key = a, str(kw)

        self.__exec_lock__.acquire()
        try:
            if key not in self.__cache_pool__:
                self.__cache_pool__[key] = self.__func__(*a, **kw)
        finally:
            self.__exec_lock__.release()

        return self.__cache_pool__[key]

    def __str__(self):
        return str(self.__func__)

    async def __core_async__(self, *a, **kw):
        key = a, str(kw)

        self.__exec_lock__.acquire()
        try:
            if key not in self.__cache_pool__:
                self.__cache_pool__[key] = await self.__func__(*a, **kw)
        finally:
            self.__exec_lock__.release()

        return self.__cache_pool__[key]


class FunctionCallerExpirationTime:

    def __init__(self, expires: int = -1):
        self.__expires = expires

        self.__exec_lock__  = threading.Lock()
        self.__cache_pool__ = {}

    def __call__(self, func: FunctionType):
        self.__func__ = func

        if asyncio.iscoroutinefunction(getattr(func, '__wrapped__', func)):
            self.__core__ = self.__core_async__

        @functools.wraps(func, updated=('__dict__', '__globals__'))
        def inner(*a, **kw):
            return self.__core__(func, *a, **kw)

        inner.__cache_pool__ = self.__cache_pool__

        return inner

    def __core__(self, func, *a, **kw):
        key = a, str(kw)

        if key not in self.__cache_pool__ or self.__cache_pool__[key][
                '__expiration_time__'] < time.time():
            with self.__exec_lock__:
                self.__cache_pool__[key] = {
                    '__return__': func(*a, **kw),
                    '__expiration_time__': time.time() + self.__expires
                }

        return self.__cache_pool__[key]['__return__']

    async def __core_async__(self, func, *a, **kw):
        key = a, str(kw)

        if key not in self.__cache_pool__ or self.__cache_pool__[key][
                '__expiration_time__'] < time.time():
            with self.__exec_lock__:
                self.__cache_pool__[key] = {
                    '__return__': await func(*a, **kw),
                    '__expiration_time__': time.time() + self.__expires
                }

        return self.__cache_pool__[key]['__return__']

    def clear_cache(self):
        self.__cache_pool__ = {}


def __getattribute__(cls: FuncCache):
    def inner(ins: cls, attr: str):
        sget = super(cls, ins).__getattribute__

        if (
                attr in ('__cache_pool__', '__not_cache__') or
                attr in cls.__not_cache__ or
                attr not in cls.__dict__
        ):
            return sget(attr)

        value = getattr(cls, attr)

        if not (callable(value) or value.__class__ in (property, classmethod)):
            return sget(attr)

        return ClassMethodCaller(cls, sget, attr, value)

    return inner


def clear_cache_pool(func) -> None:
    try:
        func.__cache_pool__.clear()
    except AttributeError:
        raise TypeError(
            f'"{func.__module__}.{func.__qualname__}" is not cached.'
        ) from None
