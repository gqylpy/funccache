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
    __shared_instance_cache__ = True
    __not_cache__ = []

    def __init__(cls, __name__: str, __bases__: tuple, __dict__: dict):
        type.__init__(cls, __name__, __bases__, __dict__)

        if cls.__shared_instance_cache__:
            cls.__cache_pool__ = {}

        cls.__getattribute__ = __getattribute__(cls)

    def __call__(cls, *a, **kw):
        ins: cls = type.__call__(cls, *a, **kw)

        if not cls.__shared_instance_cache__:
            ins.__cache_pool__ = {}

        return ins


class ClassMethodCaller:

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
            print(f'get cache: {self.name}, cls: {self.cls}')
            return x
        except KeyError:
            print(f'create cache: {self.name}, cls: {self.cls}')
            x = self.sget(self.name)(*a, **kw)
            cache_pool[key] = x
            return x

    def __str__(self):
        return f'{ClassMethodCaller.__name__}(' \
               f'{self.cls.__module__}.' \
               f'{self.cls.__name__}.{self.name})'


def __getattribute__(cls: GqylpyCache):
    def inner(ins: cls, name: str):
        sget = super(cls, ins).__getattribute__

        if name in ('__cache_pool__', '__not_cache__') or name not in cls.__dict__:
            print(f'nonsupport cache: {name}, cls: {cls.__name__}, ins: {ins}')
            return sget(name)

        if name in cls.__not_cache__:
            print(f'not cache: {name}, cls: {cls.__name__}, ins: {ins}')
            return sget(name)

        print(f'cacheable: {name}, cls: {cls.__name__}, ins: {ins}')
        return ClassMethodCaller(cls, ins, sget, name)

    return inner
