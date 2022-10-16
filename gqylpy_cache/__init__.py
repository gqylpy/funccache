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
__version__ = 1, 3, 2
__author__ = '竹永康 <gqylpy@outlook.com>'
__source__ = 'https://github.com/gqylpy/gqylpy-cache'

"""
As the name implies, "gqylpy_cache" implements the cache functionality.

Use "gqylpy_cache" as metaclass.

    >>> import gqylpy_cache
    >>> class Alpha(metaclass=gqylpy_cache):
    >>>     ...

Use "gqylpy_cache" as decorator.

    >>> import gqylpy_cache
    >>> @gqylpy_cache
    >>> def alpha():
    >>>     ...

See the documentation at https://github.com/gqylpy/gqylpy-cache.
"""


def cache(f):
    """
    Decorator, cache the return value of the function.
    To be compatible with the editor syntax hint.
    """


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    import sys

    __import__(f'{__name__}.g {__name__[7:]}')
    gcode = globals()[f'g {__name__[7:]}']

    for gname, gvalue in globals().items():
        if gname[:2] == '__' and gname != '__builtins__':
            setattr(gcode.GqylpyCache, gname, gvalue)

    gcode.GqylpyCache.   __module__ = __package__
    gcode.FunctionCaller.__module__ = __package__

    gcode.GqylpyCache.GqylpyCache = gcode.GqylpyCache
    gcode.GqylpyCache.cache       = gcode.FunctionCaller

    sys.modules[__name__] = gcode.GqylpyCache
