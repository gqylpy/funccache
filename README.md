[<img alt="LOGO" src="http://www.gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Release](https://img.shields.io/github/release/gqylpy/funccache.svg?style=flat-square")](https://github.com/gqylpy/funccache/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/funccache)](https://pypi.org/project/funccache)
[![License](https://img.shields.io/pypi/l/funccache)](https://github.com/gqylpy/funccache/blob/master/LICENSE)
[![Downloads](https://static.pepy.tech/badge/funccache)](https://pepy.tech/project/funccache)

# funccache
English | [中文](README_CN.md)

`funccache`, as its name suggests, is a framework developed by the GQYLPY team that implements function caching. It can cache the return values of specific functions or all methods defined within a class.

> _What if you have a function in your program that gets called multiple times and always returns the same value? To improve code efficiency, you might call the function once, store the return value in a variable, and then use that variable instead of repeatedly calling the function. Sound familiar? That's great! But now, we're here to introduce a more elegant solution: using the `funccache` module to directly cache function return values._

`funccache` can be used in two ways: as a metaclass to cache the return values of all methods defined in its metaclass instances, or as a decorator to cache the return values of decorated functions.

<kbd>pip3 install funccache</kbd>

### Caching Return Values of Class Methods

```python
import funccache

class Alpha(metaclass=funccache):
    ...
```
In this case, all methods and `property` attributes defined in the `Alpha` class will have their return values cached in the `__cache_pool__` attribute after being called once by an instance of the class. Subsequent calls, as long as the parameters remain the same, will directly retrieve values from `__cache_pool__` without re-executing the related code, significantly reducing program overhead and improving code readability.

By default, this caching functionality only applies to individual instances, and each instance has its own `__cache_pool__` attribute. However, if you want all instances of `Alpha` to share the same cache, you can enable the `__shared_instance_cache__` attribute:
```python
class Alpha(metaclass=funccache):
    __shared_instance_cache__ = True
```
Setting the class attribute `__shared_instance_cache__ = True` creates the `__cache_pool__` attribute in the `Alpha` class itself, rather than in each individual instance of `Alpha`.

The cache never expires by default, but you can set a time-to-live (TTL) for the cache using the class attribute `__ttl__`:
```python
class Alpha(metaclass=funccache):
    __ttl__ = 60
```

If you want a specific method or `property` to not be cached, you can add it to the `__not_cache__` list:

```python
class Alpha(metaclass=funccache):
    __not_cache__ = [method_obj_or_method_name, ...]
```
Additionally, subclasses of `Alpha` will also inherit the caching functionality.

### Caching Return Values of Functions

```python
import funccache

@funccache
def alpha():
    ...
```
In this case, the return value of the `alpha` function will be cached after it is called once. Subsequent calls, as long as the parameters remain the same, will directly retrieve the value from the cache without re-executing the `alpha` function.

The cache never expires by default, but if you want the cache to expire after a certain period, you can use `funccache.ttl`:
```python
@funccache.ttl(60)
def alpha():
    ...
```

You can even cache based on the number of calls using `funccache.count`:
```python
@funccache.count(3)
def alpha():
    ...
```

The decorator usage can also achieve singleton class behavior, as long as the instantiation parameters are consistent:
```python
@funccache
class Alpha:
    ...
```
