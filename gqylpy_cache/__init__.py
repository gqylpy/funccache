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
__version__ = 1, 0
__author__ = '竹永康 <gqylpy@outlook.com>'
__source__ = 'https://github.com/gqylpy/gqylpy-cache'

"""
The "gqylpy_cache" is used as base class.

    import gqylpy_cache
    class Alpha(gqylpy_cache):
        ...

此时，类 "Alpha" 中定义的所有方法以及property属性，在被调用一次后，其返回值都将被缓存，缓存在
"__cache_pool__" 属性中。此后的每次调用，只要参数不变，都是直接从 "__cache_pool__" 中取值，
不会重复执行相关代码，大幅减少程序功耗并提高代码可读性。

上述缓存功能默认只作用于单个实例，每个实例都有自己的 "__cache_pool__" 属性，若希望 "Alpha"
的所有实例共享同一份缓存，可启用 "__shared_instance_cache__" 属性：

    class Alpha(gqylpy_cache):
        __shared_instance_cache__ = True

若希望某个方法或property不被缓存，可将其加入到 "__not_cache__" 列表中：

    class Alpha(gqylpy_cache):
        __not_cache__ = [method1, method2, ...]

另外，此缓存功能不作用于基类中的方法和任何魔化方法。
"""
__shared_instance_cache__ = False
__not_cache__ = []


class _______歌________琪________怡_______玲_______萍_______云_______:
    import sys

    __import__(f'{__name__}.g {__name__[7:]}')
    gpack = sys.modules[__name__]
    gcode = globals()[f'g {__name__[7:]}']

    for gname, gvalue in globals().items():
        if gname[:2] == '__' and gname != '__builtins__':
            setattr(gcode.GqylpyCache, gname, gvalue)

    gcode.GqylpyCache.__module__ = __package__
    sys.modules[__name__] = gcode.GqylpyCache
