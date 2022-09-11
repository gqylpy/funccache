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

Copyright (c) 2022 GQYLPY <http://gqylpy.com>. All rights reserved.

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
__version__ = 1, 3, 1
__author__ = '竹永康 <gqylpy@outlook.com>'
__source__ = 'https://github.com/gqylpy/gqylpy-cache'

""" Use "gqylpy_cache" as metaclass.

    import gqylpy_cache
    class Alpha(metaclass=gqylpy_cache):
        ...

此时，类 "Alpha" 中定义的所有方法以及property属性，在被其实例调用一次后，其返回值都将被缓存，
缓存在"__cache_pool__" 属性中。此后的每次调用，只要参数不变，都是直接从 "__cache_pool__"
中取值，不会重复执行相关代码，大幅减少程序功耗并提高代码可读性。

上述缓存功能默认只作用于单个实例，每个实例都有自己的 "__cache_pool__" 属性，若希望 "Alpha" 
的所有实例共享同一份缓存，可启用 __shared_instance_cache__ 属性：

    class Alpha(metaclass=gqylpy_cache):
        __shared_instance_cache__ = True

设置类属性 `__shared_instance_cache__ = True` 后，属性 "__cache_pool__" 将被创建在
"Alpha" 类中，而不是 "Alpha" 的每个实例中。

若希望某个方法或property不被缓存，可将其加入到 "__not_cache__" 列表中：

    class Alpha(metaclass=gqylpy_cache):
        __not_cache__ = [method_obj_or_method_name, ...]

另外，"Alpha" 的子类也拥有上述缓存功能。
"""

""" Use "gqylpy_cache" as decorator.

    import gqylpy_cache
    @gqylpy_cache
    def alpha():
        ...

此时，函数 "alpha" 在被调用一次后，其返回值将被缓存。此后的每次调用，只要参数不变，都是直接从
缓存中取值，而不会重复执行 alpha 函数。

另外一种兼容编辑器语法提示的用法：

    from gqylpy_cache import cache
    @cache
    def alpha():
        ...
"""


def cache(f):
    ...


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    import sys

    __import__(f'{__name__}.g {__name__[7:]}')
    gcode = globals()[f'g {__name__[7:]}']

    for gname, gvalue in globals().items():
        if gname[:2] == '__' and gname != '__builtins__':
            setattr(gcode.GqylpyCache, gname, gvalue)

    gcode.GqylpyCache.__module__  = __package__
    gcode.GqylpyCache.GqylpyCache = gcode.GqylpyCache
    gcode.GqylpyCache.cache       = gcode.FunctionCaller

    sys.modules[__name__] = gcode.GqylpyCache
