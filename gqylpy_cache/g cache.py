"""
─────────────────────────────────────────────────────────────────────────────────────────────────────
─██████████████─██████████████───████████──████████─██████─────────██████████████─████████──████████─
─██░░░░░░░░░░██─██░░░░░░░░░░██───██░░░░██──██░░░░██─██░░██─────────██░░░░░░░░░░██─██░░░░██──██░░░░██─
─██░░██████████─██░░██████░░██───████░░██──██░░████─██░░██─────────██░░██████░░██─████░░██──██░░████─
─██░░██─────────██░░██──██░░██─────██░░░░██░░░░██───██░░██─────────██░░██──██░░██───██░░░░██░░░░██───
─██░░██─────────██░░██──██░░██─────████░░░░░░████───██░░██─────────██░░██████░░██───████░░░░░░████───
─██░░██──██████─██░░██──██░░██───────████░░████─────██░░██─────────██░░░░░░░░░░██─────████░░████─────
─██░░██──██░░██─██░░██──██░░██─────────██░░██───────██░░██─────────██░░██████████───────██░░██───────
─██░░██──██░░██─██░░██──██░░██─────────██░░██───────██░░██─────────██░░██───────────────██░░██───────
─██░░██████░░██─██░░██████░░████───────██░░██───────██░░██████████─██░░██───────────────██░░██───────
─██░░░░░░░░░░██─██░░░░░░░░░░░░██───────██░░██───────██░░░░░░░░░░██─██░░██───────────────██░░██───────
─██████████████─████████████████───────██████───────██████████████─██████───────────────██████───────
─────────────────────────────────────────────────────────────────────────────────────────────────────

Copyright (C) 2022 GQYLPY <http://gqylpy.com>

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
import threading


class GqylpyCache(type):
    __shared_instance_cache__ = False
    __not_cache__ = []

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
        error_methods = []

        for index, name_or_method in enumerate(__not_cache__):
            if name_or_method.__class__ is str:
                name: str = name_or_method

                if name not in list(cls.local_instance_dict_set()):
                    error_methods.append(name)
                    continue

                method = getattr(cls, name)

            else:
                method = name_or_method

                try:
                    name = __not_cache__[index] = method.__name__
                except AttributeError:
                    if method.__class__ is property:
                        name = __not_cache__[index] = method.fget.__name__
                    else:
                        name = method

                if method not in list(cls.local_instance_dict_set(v=True)):
                    error_methods.append(name)
                    continue

            if not (callable(method) or method.__class__ in (property, classmethod)):
                error_methods.append(name)
                continue

        if error_methods:
            x = f'{cls.__module__}.{cls.__name__}'
            e = error_methods if len(error_methods) > 1 else error_methods[0]
            raise cls.NotCacheDefineError(
                f'The "{__package__}" instance "{x}" has no method "{e}".'
            )

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
        cur_cls: GqylpyCache or type = baseclass or cls

        if cur_cls.__class__ is GqylpyCache:
            yield from cur_cls.__dict__.values() if v else cur_cls.__dict__
            yield from cur_cls.local_instance_dict_set(cur_cls.__base__)

    class NotCacheDefineError(Exception):
        __module__ = __package__


class ClassMethodCaller:

    def __new__(cls, cls_: GqylpyCache, ins, sget, name: str):
        method = getattr(cls_, name)

        if method.__class__ is property:
            cache_pool: dict = sget('__cache_pool__')
            try:
                x = cache_pool[name]
            except KeyError:
                x = cache_pool[name] = sget(name)
            return x

        return object.__new__(cls)

    def __init__(self, cls: GqylpyCache, ins, sget, name: str):
        self.cls = cls
        self.ins = ins
        self.sget = sget
        self.name = name

    def __call__(self, *a, **kw):
        cache_pool: dict = self.sget('__cache_pool__')
        key: tuple = self.name, a, str(kw)

        try:
            x = cache_pool[key]
        except KeyError:
            x = cache_pool[key] = self.sget(self.name)(*a, **kw)

        return x

    def __str__(self):
        return f'{ClassMethodCaller.__name__}(' \
               f'{self.cls.__module__}.' \
               f'{self.cls.__name__}.{self.name})'


def __getattribute__(cls: GqylpyCache):
    def inner(ins: cls, attr: str):
        sget = super(cls, ins).__getattribute__

        if (
                attr in ('__cache_pool__', '__not_cache__') or
                attr in sget('__not_cache__') or
                attr not in cls.__dict__
        ):
            return sget(attr)

        value = getattr(cls, attr)

        if not (callable(value) or value.__class__ in (property, classmethod)):
            return sget(attr)

        return ClassMethodCaller(cls, ins, sget, attr)

    return inner
