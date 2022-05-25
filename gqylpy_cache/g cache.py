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


class GqylpyCache:
    __shared_instance_cache__ = False
    __not_cache__ = []

    def __new__(cls, *a, **kw):
        if (
                len(a) == 1 and
                a[0].__class__ is GqylpyCache.__new__.__class__ and
                not kw
        ):
            raise NotImplementedError(
                'Due to code copyright issues, current version does not '
                'provide the function of the cache function return value. '
                'But anyway, it will be available soon in the next version.'
            )

        instance: cls = super().__new__(cls)

        if not cls.__shared_instance_cache__:
            instance.__cache_pool__ = {}
        elif not hasattr(cls, '__cache_pool__'):
            cls.__cache_pool__ = {}

        get = super(GqylpyCache, instance).__getattribute__

        for index, method in enumerate(get('__not_cache__')):
            if method.__class__ in (staticmethod, classmethod):
                get('__not_cache__')[index] = method.__func__.__name__

        return instance

    def __call__(*a):
        raise NotImplementedError(
            'Due to code copyright issues, current version does not '
            'provide the function of the cache function return value. '
            'But anyway, it will be available soon in the next version.'
        )

    def __getattribute__(self, name: str):
        get = super().__getattribute__

        if name in get('__dict__'):
            return get(name)

        no_cache: dict = get('__not_cache__')
        func = getattr(get('__class__'), name)

        if func in no_cache or name in no_cache:
            return get(name)

        if callable(func):
            return get('get_method')(get, name)

        if isinstance(func, property):
            try:
                return get('__cache_pool__')[name]
            except KeyError:
                result = get(name)
                get('__cache_pool__')[name] = result
                return result

        return get(name)

    @staticmethod
    def get_method(get, name: str):

        def inner(*a, **kw):
            key = name, a, str(kw)

            try:
                return get('__cache_pool__')[key]
            except KeyError:
                result = get(name)(*a, **kw)
                get('__cache_pool__')[key] = result
                return result

        return inner
